
from flask import render_template, url_for, make_response, jsonify, abort
from datetime import datetime, timezone
from leilao import app,db
from models import Cadastros, Adm, Produtos, Lances


@app.route('/sobre')
def sobre():
    return render_template('/paginasStatic/sobre.html')


@app.route('/como_vender')
def como_vender():
    return render_template('/paginasStatic/como_comprar.html')

@app.route('/como_comprar')
def como_comprar():
    return render_template('/paginasStatic/como_vender.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('paginaErros/404.html'), 404

@app.errorhandler(401)
def nao_autorizado(error):
    return render_template('paginaErros/401.html'), 401


@app.errorhandler(403)
def acesso_proibido(error):
    return render_template('paginaErros/403.html'), 403


