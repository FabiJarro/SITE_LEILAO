from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session, jsonify
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
app.config.from_pyfile('config.py')
   
db=SQLAlchemy(app)
migrate = Migrate(app, db)

scheduler = BackgroundScheduler()
scheduler.start()


from views import * 
from views_autenticacao import *
from views_minhaConta import *
from views_deletarEditar import *
from views_paginasStatic import *

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(debug=True)





