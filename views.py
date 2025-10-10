from flask import render_template, request, redirect, session,flash, url_for, make_response,jsonify
from datetime import datetime
from leilao import app,db
from models import Cadastros, Adm

ADMINISTRADOR="admin"
SENHA_ADM="1234"

@app.route('/')
def paginainicial():
    return render_template('index.html')


@app.route('/arearestrita')
def arearestrita():
    lista=Cadastros.query.order_by(Cadastros.id_usuario)
    # cadastros= Cadastros.query.all
    return render_template('arearestrita.html', titulo="area restrita", cadastros=lista)



@app.route("/login_AR", methods=['GET', 'POST'])
def login_AR():

    if request.method == "POST":
        usuario = request.form.get('nome_login')
        senha = request.form.get('pass_login')

        if usuario == ADMINISTRADOR and senha == SENHA_ADM:
            resposta = make_response(redirect(url_for('arearestrita')))
            # resposta.set_cookie('username', usuario, max_age=60*30)
            return resposta
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', "erro")
            return redirect(url_for('paginainicial'))

    return render_template('login_AR.html')



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


@app.route('/entrar')
def entrar():
    return render_template('entrar.html')




@app.route('/entrar_usuario', methods=['POST',])
def entrar_usuario():
    email = request.form['email']
    senha = request.form['senha']
    
    usuario=Cadastros.query.filter_by(email=email).first()
    print(request.form)
    if usuario and usuario.senha==senha:
        session['usuario_logado'] = usuario.email
        flash(f'{usuario.email} logado com sucesso!')
        print("sucesso")
        proxima_pagina = request.form.get('proxima') or url_for('paginainicial')
        return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha incorretos!')
        return redirect(url_for('entrar'))
    





#@app.route('/cadastrar')
#def cadastrar():
#    return render_template('cadastrar.html', mostrar_opcoes=False)





@app.route('/cadastrar_usuario', methods=['POST',])
def cadastrar_usuario():
    print('chegando a requisição cadastrando usuário...')
    nome=request.form['nome']
    cpf=request.form['cpf']
    data_str = request.form['data_nascimento']
    data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
    email=request.form['email']
    senha=request.form['senha']
    cep=request.form['cep']
    print("dados recebidos:", nome, cep, data_str, email, senha, cep)
    # print(f'############ {request.form}')
    # return jsonify()
    
    cadastro=Cadastros.query.filter_by(nome=nome).first()
    
    if cadastro:
        flash('cadastro existente')
        return redirect(url_for('paginainicial'))
    
    novo_cadastro=Cadastros(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, senha=senha, cep=cep)
    db.session.add(novo_cadastro)
    db.session.commit()
    print("sucesso?")
    return redirect(url_for('arearestrita'))

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html', titulo="sla")


@app.route('/salvar_produto', methods=['POST',])
def salvar_produto():
    print('chegando a requisição...')
    print(f'############ {request.form}')
    return jsonify()


