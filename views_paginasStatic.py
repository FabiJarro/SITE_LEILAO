
from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from datetime import datetime, timezone
from leilao import app,db
from models import Cadastros, Adm, Produtos, Lances


@app.route('/sobre')
def sobre():
    return render_template('/paginasStatic/sobre.html')


@app.route('/como_comprar')
def como_vender():
    return render_template('/paginasStatic/como_comprar.html')

@app.route('/como_vender')
def como_comprar():
    return render_template('/paginasStatic/como_vender.html')

