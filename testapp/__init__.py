from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 環境変数（Azure）があれば、そちらを優先して読み込む
if os.environ.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
else:
    # 環境変数がなければ、config.pyから読み込む
    app.config.from_object('testapp.config')

db = SQLAlchemy(app)
from .models import employee

import testapp.views
