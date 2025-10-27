from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from datetime import datetime
from leilao import app,db
from models import Cadastros, Adm, Produtos

ADMINISTRADOR="admin"
SENHA_ADM="1234"

@app.route('/')
def paginainicial():
    produto_destaque=Produtos.query.order_by(Produtos.id_produto).all()
    lista_produto=Produtos.query.order_by(Produtos.id_produto)
    
    # username=Cadastros.filter_by(nome=nome).first()
    
    return render_template('index.html', titulo="página inicial", produtos=lista_produto, produto_destaque=produto_destaque)


@app.route('/arearestrita')
def arearestrita():
    referer = request.referrer
    if not referer or 'login_AR' not in referer:
        return redirect(url_for('login_AR', proxima=url_for('arearestrita')))
    
    lista=Cadastros.query.order_by(Cadastros.id_usuario)
    lista_produto=Produtos.query.order_by(Produtos.id_produto)
    return render_template('arearestrita.html', titulo="area restrita", cadastros=lista, produtos=lista_produto, )

#esse referer é tipo um atalho que obtem a URL de onde que o usuario veio

@app.route('/produtos', methods=['GET'])
def getProdutos():
    #lista=Cadastros.query.order_by(Cadastros.id_usuario)
    produtos=Produtos.query.all()
    return jsonify(produtos)


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
    proxima=request.args.get('proxima')
    return render_template('entrar.html', titulo="Login", proxima=proxima)



@app.route('/entrar_usuario', methods=['POST', 'GET'])
def entrar_usuario():
    email = request.form['email']
    senha = request.form['senha']
    
    usuario=Cadastros.query.filter_by(email=email).first()
    print(request.form)
    
    if usuario==usuario and usuario.senha==senha:
        resposta = make_response(redirect(url_for('paginainicial')))
        resposta.set_cookie('email', email, max_age=60*30)
        
        session['usuario_logado'] = usuario.email
        flash(f'{usuario.email} logado com sucesso!')
        print("sucesso")
        proxima_pagina = request.form.get('proxima') or url_for('paginainicial')
        return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha incorretos!')
        return redirect(url_for('entrar'))
    
#meu autenticar com nome diferente rs (to falando do de cima)

# @app.route("/login", methods=['GET', 'POST'])
# def login():

#     if request.method == "POST":
#         usuario = request.form.get('nome_login')
#         senha = request.form.get('pass_login')

#         if usuario == USUARIO_CADASTRADO and senha == SENHA_CADASTRADO:
#             resposta = make_response(redirect(url_for('bemvindo')))
#             resposta.set_cookie('username', usuario, max_age=60*30)
#             return resposta
#         else:
#             flash('Usuário ou senha inválidos. Tente novamente.', "erro")
#             return redirect(url_for('login'))

#     return render_template('login1.html')





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
    
    cadastro = Cadastros.query.filter_by(email=email).first()
    if cadastro:
        flash('Cadastro existente.')
        return redirect(url_for('paginainicial'))
    
    
    
    cadastro=Cadastros.query.filter_by(nome=nome).first()
    
    if cadastro:
        flash('cadastro existente')
        return redirect(url_for('paginainicial'))
    
    novo_cadastro=Cadastros(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, senha=senha, cep=cep)
    db.session.add(novo_cadastro)
    db.session.commit()
    
    session['id_usuario'] = novo_cadastro.id_usuario
    
    print("sucesso?")
    
    flash ('usuario cadastrado com sucesso')
    return redirect(url_for('arearestrita'))

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html', titulo="cadastro")


@app.route('/salvar_produto', methods=['POST',])
def salvar_produto():
    print('chegando a requisição...')
    print(f'############ {request.form}')
    nome_produto=request.form['nome_produto']
    categoria_produto=request.form['categoria_produto']
    preco_produto=request.form['preco_produto']
    id_usuario = session.get('id_usuario')
    
    produto=Produtos.query.filter_by(nome_produto=nome_produto).first()
    
    if produto:
        flash('produto existente')
        return redirect(url_for('paginainicial'))
    
    if not id_usuario:
        flash ("erro: usuario não identificado")
        return redirect(url_for('entrar'))
    
    produto_existente = Produtos.query.filter_by(nome_produto=nome_produto).first()
    if produto_existente:
        flash('Produto já existente!')
        return redirect(url_for('paginainicial'))
    
    # cursor.execute("INSERT INTO produtos (nome, preco, id_usuario) VALUES (%s, %s, %s)", (nome, preco, id_usuario))
    # conexao.commit()
    
    novo_produto=Produtos(nome_produto=nome_produto, categoria_produto=categoria_produto, preco_produto=preco_produto, id_usuario=id_usuario)
    
    db.session.add(novo_produto)
    db.session.commit()
    print("sucesso?")
    flash('Produto cadstrado com sucesso')
    return redirect(url_for('arearestrita'))



@app.route('/atualizar', methods=['POST',])
def atualizar():
    cadastro= Cadastros.query.filter_by(id_usuario=request.form['id']).first()
    cadastro.nome= request.form['nome']
    cadastro.cpf=request.form['cpf']
    cadastro.data_str = request.form['data_nascimento']
    # cadastro.data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
    cadastro.email=request.form['email']
    cadastro.senha=request.form['senha']
    cadastro.cep=request.form['cep']

    
    db.session.add(cadastro)
    db.session.commit()
    
    # arquivo= request.files['arquivo']
    # uploads_path=app.config['UPLOAD_PATH']
    # timestamp=time.time()
    # deleta_arquivo(cadastro.id)
    # arquivo.save(f'{uploads_path}/capa{jogo.id}-{timestamp}.jpg')
    
    return redirect ( url_for('paginainicial'))



@app.route('/deletar/<int:id_usuario>')
def deletar(id_usuario):
    Cadastros.query.filter_by(id_usuario=id_usuario).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')
    return redirect (url_for('arearestrita'))




@app.route('/editar/<int:id_usuario>')
def editar(id_usuario):
    cadastro=Cadastros.query.filter_by(id_usuario=id_usuario).first()
    # capa_jogo=recupera_imagem(id_usuario)
    return render_template('editar.html', titulo="editando o usuario", cadastro=cadastro)
    # return render_template('editar.html', titulo="editando o usuario", cadastro=cadastro, capa_jogo=capa_jogo)


@app.route('/detalhes_produto/<int:id_produto>')
def detalhes_produto(id_produto): 
    produto=Produtos.query.filter_by(id_produto=id_produto).first()
    return render_template('detalhes_produto.html', titulo="página do produto", produto=produto)



@app.route('/fazer_lance')
def fazer_lance():
    flash('lance registrado!')
    return redirect(url_for('paginainicial'))


@app.route('/logout')
def logout():
    session.clear()
    session['usuario_logado']=None
    flash("Você foi deslogado", "info")
    resposta = make_response(redirect(url_for('entrar')))
    resposta.set_cookie('username', '', expires=0)
    return resposta