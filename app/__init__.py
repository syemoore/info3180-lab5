from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db 

app = Flask(__name__)
app.config['SECRET_KEY'] = "AsalkmasW"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:password@localhost/proj1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['UPLOADS'] = "./app/static/uploads"

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand) 

app.config.from_object(__name__)
from app import views
