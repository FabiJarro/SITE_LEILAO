
from leilao import app, db
from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from models import Cadastros, Adm, Produtos



@app.route('/minhaconta')
def minha_conta():
    return render_template('minhaconta.html', titulo="minha conta")

@app.route('/minhaconta/meus_dados/<int:id_usuario>')
def meus_dados(id_usuario):
    cadastro=Cadastros.query.filter_by(id_usuario=id_usuario).first()
    print("acessado")
    return render_template('minhaContahtmls/meus_dados.html', cadastro=cadastro)

@app.route('/minhaconta/meus_lances')
def meus_lances():
    return render_template('minhaContahtmls/meus_lances.html')

@app.route('/minhaconta/produtos_leiloados')
def produtos_leiloados():
    produtos = Produtos.query.filter_by(id_usuario=session.get('id_usuario')).all()
    return render_template('minhaContahtmls/produtos_leiloados.html', produtos=produtos)
