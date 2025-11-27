from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify, Response
from datetime import datetime, timezone
from leilao import app,db,scheduler
from models import Cadastros, Adm, Produtos, Lances, Imagens
from helpers import UsuarioForm, ProdutoForm, finalizar_leilao, hashSenha 
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import os



@app.route('/')
def paginainicial():
    print(session)
    # produto_destaque=Produtos.query.order_by(Produtos.id_produto).all()
    lista_produto=Produtos.query.order_by(Produtos.id_produto.desc()).limit(8).all()
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
            session['usuario_email'] = email_cookie
            email_logado = email_cookie
    return render_template('index.html', produtos=lista_produto, primeiro_nome=primeiro_nome)




@app.route('/arearestrita')
def arearestrita():
    referer = request.referrer
    if not referer or 'login_AR' not in referer:
        return redirect(url_for('login_AR', proxima=url_for('arearestrita')))
    
    lista=Cadastros.query.order_by(Cadastros.id_usuario)
    lista_produto=Produtos.query.order_by(Produtos.id_produto)
    
    lances=Lances.query.order_by(Lances.id_lance)
    
    return render_template('arearestrita.html', titulo="area restrita", cadastros=lista, produtos=lista_produto, lances=lances)

#esse referer é tipo um atalho que obtem a URL de onde que o usuario veio


# @app.route('/produtos', methods=['GET'])
# def getProdutos():
#     #lista=Cadastros.query.order_by(Cadastros.id_usuario)
#     produtos=Produtos.query.all()
#     return jsonify(produtos)



@app.route('/cadastrar_usuario', methods=['POST',])
def cadastrar_usuario():
    usuarioForm = UsuarioForm(request.form)
    try:
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        usuarioForm.validar()
    except ValueError as e:
        print('mensagem de errrrrrrrrrrrrrrrrrrro', e)
        return jsonify({"status": "erro" , "mensagem": str(e)})  
    
    nome=usuarioForm.nome
    cpf=usuarioForm.cpf
    rg=usuarioForm.rg
    data_str = usuarioForm.data_nascimento
    email=usuarioForm.email
    senha=hashSenha(usuarioForm.senha)
    cep=usuarioForm.cep
    numero_casa=usuarioForm.numero_casa
    rua=usuarioForm.rua
    bairro=usuarioForm.bairro
    complemento=usuarioForm.complemento
    pais =usuarioForm.pais
    cidade=usuarioForm.cidade
    estado=usuarioForm.estado
    telefone=usuarioForm.telefone
    
    try:
        data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"status": "erro", "mensagem": "Data de nascimento inválida. Use o formato YYYY-MM-DD"}), 
    
    
    if Cadastros.query.filter_by(email=email).first():
        return jsonify({"status": "erro", "mensagem": "Já existe um cadastro com esse e-mail."}), 400
            
    novo_cadastro=Cadastros(nome=nome, cpf=cpf, data_nascimento=data_nascimento, email=email, senha=senha, cep=cep, rg=rg, rua=rua, bairro=bairro, complemento=complemento, 
                            pais=pais, cidade=cidade, estado=estado, telefone=telefone)
    
    db.session.add(novo_cadastro)
    db.session.commit()
        
    session['id_usuario'] = novo_cadastro.id_usuario
        
    print("sucesso?")
    print("dados recebidos:", nome, cep, data_str, email, senha, cep)
    print("Usuário cadastrado com sucesso:", nome)
    return jsonify({"status": True, "mensagem": "Usuário cadastrado com sucesso!"}), 200



@app.route('/cadastro_usuario')
def cadastro_usuario():
    usuarioForm = UsuarioForm(request.form)
    return render_template('cadastrar_usuario.html', usuarioForm=usuarioForm)



@app.route('/cadastro_produto')
def cadastro_produto():
    produtoForm=ProdutoForm(request.form)
    return render_template('cadastrar_produto.html', produto=produtoForm)





@app.route('/cadastrar_produto', methods=['POST',])
def cadastrar_produto():
    
    produtoForm = ProdutoForm(request.form)
    try:
        produtoForm.validarProduto()
    except ValueError as e:
        print('mensagem de errrrrrrrrrrrrrrrrrrro', e)
        return jsonify({"status": "erro" , "mensagem": str(e)})  
    
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        email_logado = session.get('usuario_email') or session.get('usuario_logado')
        if email_logado:
            usuario = Cadastros.query.filter_by(email=email_logado).first()
            if usuario:
                id_usuario = usuario.id_usuario
                session['id_usuario'] = id_usuario
    
    nome_produto=produtoForm.nome_produto
    categoria_produto=produtoForm.categoria_produto
    # data_final=produtoForm.data_final
    data_final_str = produtoForm.data_final   # vem como '2025-11-04T20:03'
    data_final = datetime.strptime(data_final_str, "%Y-%m-%dT%H:%M")
    preco_produto = produtoForm.preco_produto
    descricao_produto=produtoForm.descricao_produto
    incremento_minimo=produtoForm.incremento_minimo
    id_usuario=session.get('id_usuario')
    
    if not id_usuario:
        flash ("erro: usuario não identificadooooo")
        return redirect(url_for('paginainicial'))
    
    
    produto_existente =Produtos.query.filter_by(nome_produto=nome_produto).first()
    if produto_existente:
        return jsonify({"status":"erro","mensagem":"Produto já existe"}), 400
    
    
    novo_produto=Produtos(nome_produto=nome_produto,categoria_produto=categoria_produto, preco_produto=preco_produto, descricao_produto=descricao_produto, incremento_minimo=incremento_minimo, data_final=data_final, id_usuario=id_usuario)
    
    db.session.add(novo_produto)
    print("o novo produto comitando")
    db.session.commit()
    print("coomitado:?")
    
    scheduler.add_job(
    func=finalizar_leilao,
    trigger='date',
    run_date=data_final,
    args=[novo_produto.id_produto],
    id=f"leilao_{novo_produto.id_produto}",
    replace_existing=True
    )
    
    img = request.files.get('imagem_produto')
    if img:
        filename = secure_filename(img.filename)
        mimetype = img.mimetype
        if filename and mimetype:
            nova_img = Imagens(img=img.read(), nome_imagem=filename, mimetype=mimetype, id_produto=novo_produto.id_produto, id_usuario=id_usuario)
            db.session.add(nova_img)
            db.session.commit()  
            

    # produto_destaque = Produtos.query.order_by(Produtos.id_produto).all()
    lista_produto = Produtos.query.order_by(Produtos.id_produto)

    
     
    print("sucesso?")
    print("dados recebidos:", nome_produto, categoria_produto, preco_produto, descricao_produto, incremento_minimo)
    print("Produto cadastrado com sucesso:", nome_produto)
    return jsonify({"status": True, "mensagem": "Produto cadastrado com sucesso!"})





@app.route('/detalhes_produto/<int:id_produto>')
def detalhes_produto(id_produto): 
    produto=Produtos.query.get_or_404(id_produto)
        
    lance_minimo = request.args.get('lance_minimo')
    
    ultimo_lance = Lances.query.filter_by(id_produto=id_produto).order_by(Lances.horario_lance.desc()).first()
    
    if datetime.now() > produto.data_final:
        if ultimo_lance:
            id_ganhador = ultimo_lance.id_usuario

            # Se quem está vendo é o ganhador
            if session.get('id_usuario') == id_ganhador:
                flash(f"🎉 Você venceu o leilão do produto: {produto.nome_produto}!")
            else:
                flash(f"O leilão foi encerrado! Ganhador: Usuário {id_ganhador}")
        else:
            flash("O leilão foi encerrado sem lances.")
    
    preco_inicial = float(produto.preco_produto)
    incremento = float(produto.incremento_minimo)
    valor_ultimo = float(ultimo_lance.valor_lance) if ultimo_lance else 0

    # proximo_lance = produto.preco_produto
    
    if ultimo_lance:
        proximo_lance = valor_ultimo + incremento
        lance_minimo = valor_ultimo + incremento
    else:
        proximo_lance = preco_inicial
        lance_minimo = preco_inicial
        
    return render_template('detalhes_produto.html', produto=produto, ultimo_lance=ultimo_lance, 
                           proximo_lance=proximo_lance, datetime=datetime, lance_minimo=lance_minimo)





@app.route('/fazer_lance/<int:id_produto>', methods=['POST'])
def fazer_lance(id_produto):
    produto=Produtos.query.get_or_404(id_produto)
    
    if 'usuario_logado' not in session:
        flash('login_requerido')
        return redirect(url_for('paginainicial'))
    
    if datetime.now() > produto.data_final:
        flash("Este leilão já foi encerrado!")
        return redirect(url_for('detalhes_produto', id_produto=id_produto))


    valor_lance = float(request.form['valor_lance'])
    id_usuario = session.get('usuario_logado')

    if not id_usuario:
        flash("Erro: usuário não identificado.")
        return redirect(url_for('paginainicial'))


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
    return redirect(url_for('paginainicial', id_produto=id_produto))




@app.route('/<int:id_imagem>')
def get_img(id_imagem):
    img= Imagens.query.filter_by(id_imagem=id_imagem).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.img, mimetype=img.mimetype)

@app.route('/todosProdutos')
def todosProdutos():
    todosProdutos=Produtos.query.order_by(Produtos.id_produto).all()
    lista_produto=Produtos.query.order_by(Produtos.id_produto)

    return render_template('todosProdutos.html', produtos=lista_produto, todosProdutos=todosProdutos)



@app.route('/produtos')
def produtos():
    nome_produto = request.args.get('nome_produto', '').strip()        
    query = Produtos.query

    if nome_produto: query = query.filter(or_(Produtos.nome_produto.ilike(f"%{nome_produto}%"), Produtos.categoria_produto.ilike(f"%{nome_produto}%")))

    lista = query.order_by(Produtos.id_produto).all()

    return render_template('todosProdutos.html', produtos=lista, nome_produto=nome_produto)




@app.route('/denunciar/<int:id_produto>', methods=['POST'])
def denunciar(id_produto):
    if 'usuario_logado' not in session:
        return redirect('/login')

    denuncia= f"denuncia_{id_produto}"

    if session.get(denuncia):
        flash("Você já denunciou este produto.")
        return redirect(url_for('detalhes_produto', id_produto=id_produto))

    produto = Produtos.query.get(id_produto)

    if not produto:
        flash("Produto não encontrado.")
        return redirect('/')

    produto.denuncias += 1
    db.session.commit()

    session[denuncia] = True  

    flash("Denúncia enviada com sucesso.")
    return redirect(url_for('detalhes_produto', id_produto=id_produto))



