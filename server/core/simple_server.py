import logging
import ssl
from datetime import datetime
from functools import wraps
import bottle
from beaker.middleware import SessionMiddleware
from bottle import (
    response,
    run,
    request,
    ServerAdapter,
    get
)
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
from apscheduler.schedulers.background import BackgroundScheduler
# import project files
from core.addbooking import add_ongoing_booking
from utils.log import write_server_log
from core.check_online_booking import CheckOnlineBooking
from core.update_department_availability import UpdateDepartmentAvailabilities
from config.configuration_manager import ConfigurationManager

config = ConfigurationManager()
# load configuration's parameters
COB_CRON_INTERVAL = int(config.active_configuration['COB_CRON_INTERVAL'])
UDA_CRON_INTERVAL = int(config.active_configuration['UDA_CRON_INTERVAL'])
PORT = int(config.active_configuration['PORT'])
HOST = config.active_configuration['HOST']
CERTIFICATE_PATH = config.active_configuration['CERTIFICATE_PATH']
PRIVATE_KEY_PATH = config.active_configuration['PRIVATE_KEY_PATH']
DEBUG = config.active_configuration['DEBUG']
DEPT_AVAILABILITIES_CACHE_MAX_AGE = config.active_configuration['DEPT_AVAILABILITIES_CACHE_MAX_AGE']

logger = logging.getLogger('coMedServer')

# set up the logger
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('server.log')
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# set up background cron to check online booking every hour
scheduler = BackgroundScheduler()
cob = CheckOnlineBooking()
uda = UpdateDepartmentAvailabilities()


@scheduler.scheduled_job('interval', minutes=COB_CRON_INTERVAL, next_run_time=datetime.now())
def check_online_booking_cron():
    cob.check_online_booking_job()


@scheduler.scheduled_job('interval', minutes=UDA_CRON_INTERVAL, next_run_time=datetime.now())
def update_department_availabilities_cron():
    uda.update_department_availabilities_job()


def log_to_logger(fn):
    """
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    """

    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        # modify this to log exactly what you need:
        logger.info('%s %s %s %s %s' % (request.remote_addr,
                                        request_time,
                                        request.method,
                                        request.url,
                                        response.status))
        return actual_response

    return _log_to_logger


# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(ServerAdapter):

    def run(self, handler):
        server = wsgi.Server((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter(CERTIFICATE_PATH, PRIVATE_KEY_PATH)

        # By default, the server will allow negotiations with extremely old protocols
        # that are susceptible to attacks, so we only allow TLSv1.2
        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1
        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1_1

        try:
            server.start()
        finally:
            server.stop()


# Create the default bottle app and then wrap it around
# a beaker middleware and send it back to bottle to run
session_opts = {
    "session.type": "file",
    "session.cookie_expires": True,
    "session.data_dir": "./data",
    "session.auto": True,
}
bottle_app = bottle.app()
bottle_app.install(log_to_logger)
app = SessionMiddleware(bottle_app, session_opts)


@bottle.route('/<:re:.*>', method='OPTIONS')
def enable_cors_generic_route():
    """
    This route takes priority over all others. So any request with an OPTIONS
    method will be handled by this function.

    See: https://github.com/bottlepy/bottle/issues/402

    NOTE: This means we won't 404 any invalid path that is an OPTIONS request.
    """
    add_cors_headers()


@bottle.hook('after_request')
def enable_cors_after_request_hook():
    """
    This executes after every route. We use it to attach CORS headers when
    applicable.
    """
    add_cors_headers()


def add_cors_headers():
    bottle.response.headers['Access-Control-Allow-Origin'] = 'https://www.commissionmedicale.fr'
    bottle.response.headers['Access-Control-Allow-Methods'] = \
        'GET, POST, PUT, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@bottle.route('/booking/new', method=['POST'])
def new_booking():
    write_server_log('------------Add new booking ------------\r\n')
    write_server_log(request)
    write_server_log(request.json)
    add_ongoing_booking(request.json)
    write_server_log('------------Booking added------------ \r\n')


@get('/department_availabilities')
def get_department_availabilities():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'max-age=' + DEPT_AVAILABILITIES_CACHE_MAX_AGE
    with open('../json/department_availabilities.json', "r", encoding='utf-8') as da_file_handler:
        return da_file_handler.read()


def shutdown_cron_jobs():
    cob.cancelJob = True
    uda.cancelJob = True
    scheduler.remove_all_jobs()
    scheduler.shutdown()


if __name__ == "__main__":
    write_server_log(f'Server https://{HOST}:{PORT} running...')
    scheduler.start()
    run(app=app, host=HOST, port=PORT, server=SSLCherryPyServer, debug=DEBUG)
    # if we reach here, run has exited (Ctrl-C)
    # clean up (join) threads here
    shutdown_cron_jobs()
