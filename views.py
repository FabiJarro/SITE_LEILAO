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
    email_logado = session.get('usuario_logado')
    primeiro_nome = None
    
    if email_logado:
        usuario = Cadastros.query.filter_by(email=email_logado).first()
        if usuario:
            primeiro_nome = usuario.nome.split()[0]
        print(primeiro_nome)
    else:
        email_cookie=request.cookies.get('usuario_email')
        if email_cookie:
            session['usuario_logado'] = email_cookie
            email_logado = email_cookie
    return render_template('index.html', titulo="página inicial", produtos=lista_produto, produto_destaque=produto_destaque, primeiro_nome=primeiro_nome)


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


@app.route('/detalhes_produto/<int:id_produto>')
def detalhes_produto(id_produto): 
    produto=Produtos.query.filter_by(id_produto=id_produto).first()
    return render_template('detalhes_produto.html', titulo="página do produto", produto=produto)




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


@app.route('/fazer_lance')
def fazer_lance():
    flash('lance registrado!')
    return redirect(url_for('paginainicial'))

