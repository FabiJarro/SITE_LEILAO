
from leilao import app, db
from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify, abort
from models import Cadastros, Adm, Produtos



@app.route('/minhaconta')
def minha_conta():
    return render_template('minhaconta.html', titulo="minha conta")





@app.route('/minhaconta/meus_dados')
def meus_dados():
    email_logado = session.get('usuario_email')
    
    # if 'usuario_email' not in session:
    #     return redirect(url_for('nao_autorizado'))
    
    usuario = Cadastros.query.filter_by(email=session['usuario_logado']).first()
    cadastro = Cadastros.query.filter_by(email=email_logado).first()
    if not cadastro:
        print("acessado")
    return render_template('minhaContahtmls/meus_dados.html', cadastro=cadastro)


#DEU CERTO CARAMBA


@app.route('/minhaconta/produtos_leiloados')
def produtos_leiloados():
    
    email_logado = session.get('usuario_logado')
    usuario = Cadastros.query.filter_by(email=session['usuario_logado']).first()
    produtos = Produtos.query.filter_by(id_usuario=usuario.id_usuario).all()
    
    if 'usuario_logado' not in session:
        return redirect(url_for('nao_autorizado'))
    
    if not usuario:
        return redirect(url_for('page_not_found'))
    return render_template('minhaContahtmls/produtos_leiloados.html', produtos=produtos)


@app.route('/minhaconta/meus_lances')
def meus_lances():
    abort(404)
    
