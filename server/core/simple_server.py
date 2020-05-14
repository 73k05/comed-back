import bottle
from bottle import Bottle, run, request, response

from addbooking import add_ongoing_booking


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    @staticmethod
    def apply(fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers[
                'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = Bottle()


@app.route('/booking/new', method=['OPTIONS', 'POST'])
def hello():
    print('<b>Hello {{json}}</b>!', request.json)
    add_ongoing_booking(request.json)


app.install(EnableCors())
run(app, host='127.0.0.1', port=9001)

print('Server {{host}}:{{port}} running...')
