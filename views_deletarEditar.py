from flask import render_template, request, redirect, session, flash, url_for, make_response, jsonify
from datetime import datetime, timezone
from leilao import app,db

from models import Cadastros, Adm, Produtos, Lances


@app.route('/atualizarUsuario', methods=['POST',])
def atualizarUsuario():
    cadastro=Cadastros.query.filter_by(id_usuario=request.form['id_usuario']).first()
    cadastro.nome= request.form['nome']
    cadastro.cpf=request.form['cpf']
    cadastro.data_str = request.form['data_nascimento']
    # cadastro.data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
    cadastro.email=request.form['email']
    cadastro.senha=request.form['senha']
    cadastro.cep=request.form['cep']
    db.session.add(cadastro)
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

@app.route('/deletar/<int:id_produto>')
def deletarProduto(id_produto):
    produto= Produtos.query.get_or_404(id_lance)
    db.session.delete(produto)
    db.session.commit()
    flash('produto deletado')
    return redirect (url_for('arearestrita'))


@app.route('/editar/<int:id_produto>')
def editarProduto(id_produto):
    cadastro=Cadastros.query.filter_by(id_usuario=id_usuario).first()
    return render_template('editar/editarProduto.html', titulo="editando o usuario", cadastro=cadastro)


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
    # capa_jogo=recupera_imagem(id_usuario)
    return render_template('editar.html', titulo="editando o usuario", cadastro=cadastro)
    # return render_template('editar.html', titulo="editando o usuario", cadastro=cadastro, capa_jogo=capa_jogo)

