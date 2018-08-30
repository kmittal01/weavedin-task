from app.config.base import hostname, port
from app.extensions import app, get_new_session
from app.token.controller import decode_token_ctrl
from app.token.routes import token
from app.user.routes import user_api
from app.item.routes import item_api
from app.extensions import g
from flask import request
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell, Server as BaseServer
from app.extensions import db

app.register_blueprint(user_api)
app.register_blueprint(item_api)
app.register_blueprint(token)

auth_check_ignore_list = ['user_api.create_user', 'token_api.get_token']


manager = Manager(app)

shell_banner = """
Welcome to your Flask CLI environment.
The following variables are available to use:
db            -> Flask-Sqlalchemy extension
All the models, apis and schemas
"""


def make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    context = {'app': app, 'db': db}
    return context


class Server(BaseServer):
    def __call__(self, app, host, port, use_debugger, use_reloader, threaded,
                 processes, passthrough_errors):
        super(Server, self).__call__(app, host, port, use_debugger,
                                     use_reloader, threaded, processes,
                                     passthrough_errors)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(use_debugger=True, port=port if port else 5001, host=hostname))
manager.add_command('shell', Shell(banner=shell_banner,
                                   make_context=make_context))


@app.before_request
def before_request():
    g.session = get_new_session()
    auth_token = request.headers.get('token')
    if request.endpoint not in auth_check_ignore_list:
        g.restricted_endpoint = True
        user = decode_token_ctrl(auth_token)
        g.user = user
    else:
        g.restricted_endpoint = False


@app.after_request
def after_request(res):
    g.session.close()
    return res


if __name__ == '__main__':
    manager.run()
