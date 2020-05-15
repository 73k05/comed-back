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
    default_app,
)
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter

from addbooking import add_ongoing_booking
from log import write_server_log

logger = logging.getLogger('coMedServer')

# set up the logger
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('server.log')
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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


# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(ServerAdapter):

    def run(self, handler):
        server = wsgi.Server((self.host, self.port), handler)
        # server.ssl_adapter = BuiltinSSLAdapter("./ssl/cacert.pem", "./ssl/privkey.pem")
        server.ssl_adapter = BuiltinSSLAdapter("/etc/letsencrypt/live/73k05.xyz/cert.pem",
                                               "/etc/letsencrypt/live/73k05.xyz/privkey.pem")

        # By default, the server will allow negotiations with extremely old protocols
        # that are susceptible to attacks, so we only allow TLSv1.2
        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1
        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1_1

        try:
            server.start()
        finally:
            server.stop()


# app = Bottle()
bottle_app = default_app()

# Create the default bottle app and then wrap it around
# a beaker middleware and send it back to bottle to run
session_opts = {
    "session.type": "file",
    "session.cookie_expires": True,
    "session.data_dir": "./data",
    "session.auto": True,
}
bottle_app.install(EnableCors())
bottle_app.install(log_to_logger)

app = SessionMiddleware(bottle_app, session_opts)


@bottle.route('/booking/new', method=['POST'])
def new_booking():
    write_server_log('------------Add new booking ------------\r\n')
    write_server_log(request)
    write_server_log(request.json)
    add_ongoing_booking(request.json)
    write_server_log('------------Booking added------------ \r\n')


port = 443
host = '0.0.0.0'
if __name__ == "__main__":
    write_server_log(f'Server https://{host}:{port} running...')
    run(app=app, host=host, port=port, server=SSLCherryPyServer)
# run(app, host=host, port=port, server='cheroot', options=options)
