from leilao import app, db
from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from models import Cadastros, Adm, Produtos

ADMINISTRADOR="admin"
SENHA_ADM="1234"

@app.route('/entrar_usuario', methods=['POST', 'GET'])
def entrar_usuario():
    email = request.form['email']
    senha = request.form['senha']
    
    usuario=Cadastros.query.filter_by(email=email).first()
    print(request.form)
    
    if usuario==usuario and usuario.senha==senha:
        session['usuario_logado'] = usuario.email
        session.permanent = True 
        resposta = make_response(redirect(url_for('paginainicial')))
        resposta.set_cookie('usuario_email', usuario.email)
        flash(f'{usuario.nome.split()[0]} logado com sucesso!')
        print("sucesso")
        proxima_pagina = request.form.get('proxima') or url_for('paginainicial')
        return resposta
    else:
        flash('Usuário ou senha incorretos!')
        return redirect(url_for('entrar'))
    
@app.route('/entrar')
def entrar():
    proxima=request.args.get('proxima')
    return render_template('entrar.html', titulo="Login", proxima=proxima)


# @app.route('/login_AR')
# def login_AR():
#     proxima=request.args.get('proxima')
#     return render_template('arearestrita.html', proxima=proxima)


# @app.route('/autenticar_AR', methods=['POST',])
# def autenticar_AR():
#     adm=Adm.query.filter_by(email=request.form['adm']).first()

#     if adm and request.form['senha'] == adm.senha:
#         session['adm_logado'] = adm.email
#         flash(adm.email + ' logado com sucesso!')
#         proxima_pagina = request.form.get('proxima')
#         return redirect(proxima_pagina)
#     else:
#         flash('Usuário ou senha incorretos!')
#         return redirect(url_for('login_AR'))


@app.route("/login_AR", methods=['GET', 'POST'])
def login_AR():
    proxima=request.args.get('proxima') or url_for('arearestrita')
    
    if request.method == "POST":
        adm= request.form.get('adm_login')
        senha = request.form.get('pass_login')

        if adm== ADMINISTRADOR and senha == SENHA_ADM:
            return redirect(proxima)
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', "erro")
            return redirect(url_for('login_AR'), proxima=proxima)

    return render_template('login_AR.html', titulo="login- area restrita", proxima=proxima)


@app.route('/logout')
def logout():
    session.clear()
    session['usuario_logado']=None
    flash("Você foi deslogado", "info")
    resposta = make_response(redirect(url_for('paginainicial')))
    resposta.set_cookie('usuario_email', '', expires=0)
    return resposta


