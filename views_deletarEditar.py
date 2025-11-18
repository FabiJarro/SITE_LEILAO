from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from datetime import datetime, timezone
from leilao import app,db

from models import Cadastros, Adm, Produtos, Lances, Imagens


@app.route('/atualizarUsuario', methods=['POST',])
def atualizarUsuario():
    cadastro=Cadastros.query.filter_by(id_usuario=request.form['id_usuario']).first()
    cadastro.nome= request.form['nome']
    cadastro.cpf=request.form['cpf']
    cadastro.rg=request.form['rg']
    cadastro.data_str = request.form['data_nascimento']
    # cadastro.data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
    cadastro.email=request.form['email']
    cadastro.senha=request.form['senha']
    cadastro.cep=request.form['cep']
    cadastro.rua=request.form['rua']
    cadastro.bairro=request.form['bairro']
    cadastro.complemento=request.form['complemento']
    cadastro.pais=request.form['pais']
    cadastro.cidade=request.form['cidade']
    cadastro.telefone=request.form['telefone']
    cadastro.estado=request.form['estado']
    db.session.add(cadastro)
    db.session.commit()
    return redirect (url_for('paginainicial'))



# @app.route('/atualizarProduto', methods=['POST',])
# def atualizarProduto():
#     produto=Produtos.query.filter_by(id_produto=request.form['id_produto']).first()
#     produto.nome_produto= request.form['nome_produto']
#     produto.categoria_produto=request.form['categoria_produto']
#     produto.preco_produto = request.form['preco_produto']
#     produto.incremento_minimo=request.form['incremento_minimo']
#     produto.descricao_produto=request.form['descricao_produto']

#     img=Imagens.query.filter_by(id_imagem=request.form['id_imagem']).first()
#     img.imagem_produto= request.form['imagem_produto']
    
#     db.session.add(produto)
#     db.session.add(img)
#     db.session.commit()
    
#     return redirect (url_for('paginainicial'))

@app.route('/atualizarProduto', methods=['POST',])
def atualizarProduto():
    produto=Produtos.query.filter_by(id_produto=request.form['id_produto']).first()
    produto.nome_produto= request.form['nome_produto']
    produto.categoria_produto=request.form['categoria_produto']
    produto.preco_produto = request.form['preco_produto']
    produto.incremento_minimo=request.form['incremento_minimo']
    produto.descricao_produto=request.form['descricao_produto']
    # produto.imagens=request.form['imagem_produto']
        
    
    db.session.add(produto)
    db.session.commit()
    
    return redirect (url_for('paginainicial'))





@app.route('/deletar/<int:id_usuario>')
def deletarUsuario(id_usuario):
    usuario = Cadastros.query.get_or_404(id_usuario)
    # Cadastros.query.filter_by(id_usuario=id_usuario).delete()
    db.session.delete(usuario)
    db.session.commit()
    flash('usuario deletado')
    return redirect (url_for('arearestrita'))



@app.route('/editarUsuario/<int:id_usuario>')
def editarUsuario(id_usuario):
    cadastro=Cadastros.query.filter_by(id_usuario=id_usuario).first()
    return render_template('/editar/editarUsuario.html', cadastro=cadastro)

    
    
#_______________________________________________________________________________

@app.route('/deletarProduto/<int:id_produto>')
def deletarProduto(id_produto):
    produto=Produtos.query.get_or_404(id_produto)
    db.session.delete(produto)
    db.session.commit()
    flash('produto deletado')
    return redirect (url_for('arearestrita'))


@app.route('/editarProduto/<int:id_produto>')
def editarProduto(id_produto):
    produto=Produtos.query.filter_by(id_produto=id_produto).first()
    # imagens = Imagens.query.filter_by(id_imagem=id_imagem).first()
    return render_template('editar/editarProduto.html', produto=produto)


#_______________________________________________________

@app.route('/deletarLance/<int:id_lance>')
def deletarLance(id_lance):
    lance= Lances.query.get_or_404(id_lance)
    db.session.delete(lance)
    db.session.commit()
    flash('lance deletado')
    return redirect (url_for('arearestrita'))


@app.route('/editarLance/<int:id_lance>')
def editarLance(id_lance):
    cadastro=Cadastros.query.filter_by(id_usuario=id_usuario).first()
    return render_template('editar.html', titulo="editando o usuario", cadastro=cadastro)

