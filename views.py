from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from datetime import datetime, timezone
from leilao import app,db
from models import Cadastros, Adm, Produtos, Lances
from helpers import UsuarioForm

ADMINISTRADOR="admin"
SENHA_ADM="1234"

@app.route('/')
def paginainicial():
    print(session)
    produto_destaque=Produtos.query.order_by(Produtos.id_produto).all()
    lista_produto=Produtos.query.order_by(Produtos.id_produto)
    email_logado = session.get('usuario_email')
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
    return render_template('index.html', produtos=lista_produto, produto_destaque=produto_destaque, primeiro_nome=primeiro_nome)




@app.route('/arearestrita')
def arearestrita():
    referer = request.referrer
    if not referer or 'login_AR' not in referer:
        return redirect(url_for('login_AR', proxima=url_for('arearestrita')))
    
    lista=Cadastros.query.order_by(Cadastros.id_usuario)
    lista_produto=Produtos.query.order_by(Produtos.id_produto)
    
    lances=Lances.query.order_by(Lances.id_lance)
    
    # lances = db.session.query(
    # Lances.id_lance,
    # Lances.id_usuario,
    # Lances.id_produto,
    # Lances.valor_lance,
    # Lances.horario_lance,
    # ).join(Produtos, Lances.id_produto == Produtos.id_produto) .join(Cadastros, Lances.id_usuario == Cadastros.id_usuario).order_by(Lances.id_lance.desc()).all()
    
    return render_template('arearestrita.html', titulo="area restrita", cadastros=lista, produtos=lista_produto, lances=lances)

#esse referer é tipo um atalho que obtem a URL de onde que o usuario veio

@app.route('/produtos', methods=['GET'])
def getProdutos():
    #lista=Cadastros.query.order_by(Cadastros.id_usuario)
    produtos=Produtos.query.all()
    return jsonify(produtos)



# @app.route('/cadastrar_usuario', methods=['POST',])
# def cadastrar_usuario():
#     usuarioForm = UsuarioForm(request.form)
#     try:
#         print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#         usuarioForm.validar()
#     except ValueError as e:
#         print('mensagem de errrrrrrrrrrrrrrrrrrro', e)
#         return jsonify({"status": False, "mensagem": str(e)})  
    
#     nome=usuarioForm.nome
#     cpf=usuarioForm.cpf
#     data_str = usuarioForm.data_nascimento
#     email=usuarioForm.email
#     senha=usuarioForm.senha
#     cep=usuarioForm.cep
    
#     try:
#         data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
#     except ValueError:
#         return jsonify({"status": False, "mensagem": "Data de nascimento inválida. Use o formato YYYY-MM-DD"}), 
    
    
#     if Cadastros.query.filter_by(email=email).first():
#         return jsonify({"status": "erro", "mensagem": "Já existe um cadastro com esse e-mail."}), 400
            
#     novo_cadastro=Cadastros(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, senha=senha, cep=cep)
    
#     db.session.add(novo_cadastro)
#     db.session.commit()
        
#     session['id_usuario'] = novo_cadastro.id_usuario
        
#     print("sucesso?")
#     flash('Usuário cadastrado com sucesso!')
#     print("dados recebidos:", nome, cep, data_str, email, senha, cep)
#     print("Usuário cadastrado com sucesso:", nome)
#     return jsonify({"status": True, "mensagem": "Usuário cadastrado com sucesso!"}), 200

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    usuarioForm = UsuarioForm(request.form)
    
    try:
        usuarioForm.validar()
    except ValueError as e:
        # Retorna JSON com a mensagem de erro
        return jsonify({"sucesso": False, "mensagem": str(e)}), 400

    # verifica duplicidade de e-mail
    if Cadastros.query.filter_by(email=usuarioForm.email).first():
        return jsonify({"sucesso": False, "mensagem": "Já existe um cadastro com esse e-mail."}), 400

    # se tudo estiver certo, cria o usuário
    try:
        data_nascimento = datetime.strptime(usuarioForm.data_nascimento, "%Y-%m-%d").date()
        novo_cadastro = Cadastros(
            nome=usuarioForm.nome,
            cpf=usuarioForm.cpf,
            data_nascimento=data_nascimento,
            email=usuarioForm.email,
            senha=usuarioForm.senha,
            cep=usuarioForm.cep
        )
        db.session.add(novo_cadastro)
        db.session.commit()
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro ao salvar no banco: {e}"}), 500

    return jsonify({"sucesso": True, "mensagem": "Usuário cadastrado com sucesso!"}), 200


@app.route('/cadastro_usuario')
def cadastro_usuario():
    usuarioForm = UsuarioForm(request.form)
    return render_template('cadastrar_usuario.html', form=usuarioForm)



@app.route('/cadastrar_produto')
def cadastro_produto():
    formProduto=FormularioProduto(request.form)
    return render_template('cadastrar_produto.html', formProduto=formProduto)


# @app.route('/cadastrar_produto', methods=['POST',])
# def salvar_produto():
#     print('chegando a requisição...')
#     print(f'############ {request.form}')
#     nome_produto=request.form['nome_produto']
#     categoria_produto=request.form['categoria_produto']
#     preco_produto=request.form['preco_produto']
#     incremento_minimo=request.form['incremento_minimo']
#     id_usuario = session.get('id_usuario')
    
#     produto=Produtos.query.filter_by(nome_produto=nome_produto).first()
    
#     if produto:
#         flash('produto existente')
#         return redirect(url_for('paginainicial'))
    
#     if not id_usuario:
#         flash ("erro: usuario não identificado")
#         return redirect(url_for('entrar'))
    
#     produto_existente = Produtos.query.filter_by(nome_produto=nome_produto).first()
#     if produto_existente:
#         flash('Produto já existente!')
#         return redirect(url_for('paginainicial'))
    
#     # cursor.execute("INSERT INTO produtos (nome, preco, id_usuario) VALUES (%s, %s, %s)", (nome, preco, id_usuario))
#     # conexao.commit()
    
#     novo_produto=Produtos(nome_produto=nome_produto, categoria_produto=categoria_produto, preco_produto=preco_produto, 
#                           incremento_minimo=incremento_minimo, id_usuario=id_usuario)
    
#     db.session.add(novo_produto)
#     db.session.commit()
#     print("sucesso?")
#     flash('Produto cadstrado com sucesso')
#     return redirect(url_for('arearestrita'))




@app.route('/detalhes_produto/<int:id_produto>')
def detalhes_produto(id_produto): 
    produto=Produtos.query.get_or_404(id_produto)
        
    lance_minimo = request.args.get('lance_minimo')
    
    ultimo_lance = Lances.query.filter_by(id_produto=id_produto).order_by(Lances.horario_lance.desc()).first()
    
    proximo_lance = produto.preco_produto
    if ultimo_lance:
        proximo_lance = ultimo_lance.valor_lance + produto.incremento_minimo

    lance_minimo = float(produto.preco_produto)
    if ultimo_lance:
        lance_minimo = float(ultimo_lance.valor_lance) + float(produto.incremento_minimo)

    return render_template('detalhes_produto.html', produto=produto, ultimo_lance=ultimo_lance, 
                           proximo_lance=proximo_lance, datetime=datetime, lance_minimo=lance_minimo)




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
    
    return redirect ( url_for('paginainicial'))





@app.route('/fazer_lance/<int:id_produto>', methods=['POST'])
def fazer_lance(id_produto):
    produto=Produtos.query.get_or_404(id_produto)
    
    if 'usuario_logado' not in session:
        flash('login_requerido')
    return redirect(url_for('paginainicial'))

    valor_lance = float(request.form['valor_lance'])
    id_usuario = session.get('usuario_logado')


    ultimo_lance = (
        Lances.query.filter_by(id_produto=id_produto)
        .order_by(Lances.horario_lance.desc())
        .first()
    )

    lance_minimo = float(produto.preco_produto)
    if ultimo_lance:
        lance_minimo = float(ultimo_lance.valor_lance) + float(produto.incremento_minimo)
    if valor_lance <lance_minimo:
        flash(f'O valor mínimo para este lance é R$ {lance_minimo:.2f}')
        return redirect(url_for('detalhes_produto', id_produto=id_produto, lance_minimo=lance_minimo))

    novo_lance = Lances( valor_lance=valor_lance, id_produto=id_produto, id_usuario=id_usuario)

    print(f"Lance recebido: R${valor_lance}")
    db.session.add(novo_lance) 
    db.session.commit()

    flash('Lance registrado com sucesso!')
    return redirect(url_for('detalhes_produto', id_produto=id_produto))

