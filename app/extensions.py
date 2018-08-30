from flask import Flask, g
from sqlalchemy import create_engine
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
from config.base import DB_URL
from sqlalchemy_utils import GUID
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

engine = create_engine(DB_URL, pool_size=50, max_overflow=0)


def get_new_session():
    DBSession = orm.scoped_session(orm.sessionmaker(bind=engine))
    session = DBSession()
    return session


db = SQLAlchemy(app)
db.GUID = GUID
migrate = Migrate(app, db)

ma = Marshmallow(app)

