from leilao import app, db
from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from models import Cadastros, Adm, Produtos, Lances
from helpers import hashSenha


@app.route('/entrar_usuario', methods=['POST', 'GET'])
def entrar_usuario():
    email = request.form['email']
    senha = hashSenha(request.form['senha'])
    
    usuario=Cadastros.query.filter_by(email=email).first()
    print(request.form)
    
    if usuario==usuario and usuario.senha==senha:
        session['usuario_email']= usuario.email
        session['usuario_logado'] = usuario.id_usuario

        session.permanent = True 
        resposta = make_response(redirect(url_for('paginainicial')))
        resposta.set_cookie('usuario_email', usuario.email)
        flash(f'{usuario.nome.split()[0]} logado com sucesso!')
        print("sucesso")
        proxima_pagina = request.form.get('proxima') or url_for('paginainicial')
        return resposta
    else:
        flash('Usuário ou senha incorretos!')
        return "erro", 401
    
@app.route('/entrar')
def entrar():
    proxima=request.args.get('proxima')
    return render_template('entrar.html', titulo="Login", proxima=proxima)




@app.route("/login_AR", methods=['GET', 'POST'])
def login_AR():
    proxima = request.args.get('proxima') or url_for('arearestrita')

    if request.method == "POST":
        email_adm = request.form['email_adm']
        senha_adm = hashSenha(request.form['senha_adm'])
        adm = Adm.query.filter_by(email=email_adm).first()
        
        if adm and senha_adm == adm.senha:
            return redirect(proxima)
        else:
            flash('Usuário ou senha inválidos. Tente novamente.')
            return redirect(url_for('login_AR'))

    return render_template('login_AR.html', proxima=proxima)



@app.route('/logout')
def logout():
    session.clear()
    flash("Você foi deslogado")
    resposta = make_response(redirect(url_for('paginainicial')))
    resposta.set_cookie('usuario_email', '', expires=0)
    return resposta


