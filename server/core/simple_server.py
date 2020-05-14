import bottle
from bottle import Bottle, run, request, response

from addbooking import add_ongoing_booking
from log import write_server_log
from datetime import datetime
from functools import wraps
import logging

logger = logging.getLogger('coMedServer')

# set up the logger
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('server.log')
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def log_to_logger(fn):
    '''
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    '''

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


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    @staticmethod
    def apply(fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = 'https://www.commissionmedicale.fr'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers[
                'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = Bottle()
app.install(EnableCors())
app.install(log_to_logger)


@app.route('/booking/new', method=['OPTIONS', 'POST'])
def hello():
    write_server_log('------------Add new booking ------------\r\n')
    write_server_log(request.json)
    add_ongoing_booking(request.json)
    write_server_log('------------Booking added------------ \r\n')


port = 9001
host = '0.0.0.0'
write_server_log(f'Server {host}:{port} running...')
run(app, host=host, port=port)
