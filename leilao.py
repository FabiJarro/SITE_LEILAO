from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')   


db=SQLAlchemy(app)

from views import * 
from views_autenticacao import *
from views_minhaConta import *

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5000)
    # app.permanent_session_lifetime = timedelta(hours=1)
    app.run(debug=True)


