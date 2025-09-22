from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key ='143'

# SGBD='mysql+mysqlconnector'
# usuario='root'
# senha='Fofurica.10'
# servidor='localhost'
# database='cadastro'



ADMINISTRADOR="admin"
SENHA_ADM="123"


SGBD='mysql+mysqlconnector'
usuario='root'
senha='Fofurica.10'
servidor='localhost'
database='teste_cadastro'
        
app.config['SQLALCHEMY_DATABASE_URI']= f'{SGBD}://{usuario}:{senha}@{servidor}/{database}'

     



db=SQLAlchemy(app)


@app.route('/')
def paginainicial():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        usuario = request.form.get('nome_login')
        senha = request.form.get('pass_login')

        if usuario == ADMINISTRADOR and senha == SENHA_ADM:
            resposta = make_response(redirect(url_for('paginainicial')))
            # resposta.set_cookie('username', usuario, max_age=60*30)
            return resposta
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', "erro")
            return redirect(url_for('paginainicial'))

    return render_template('entrar.html')





@app.route('/entrar')
def entrar():
    return render_template('entrar.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')
    
    
    
    
    

@app.route('/arearestrita')
def arearestrita():
    return render_template('arearestrita.html')

@app.route('/opcoes_vender_ou_comprar')
def opcoes_vender_ou_comprar():
    return render_template('arearestrita.html')


@app.route('/salvar_cadastro', methods=['POST',])
def salvar_cadastro():
    # nome=request.form['nome']
    # email=request.form['email']
    # senha=request.form['senha']
    
    # jogo=Jogos.query.filter_by(nome=nome).first()
    
    # if jogo:
    #     flash('Jogo já existente')
    #     return redirect(url_for('index'))
    
    # novo_jogo=Jogos(nome=nome, categoria=categoria,console=console)
    # db.session.add(novo_jogo)
    # db.session.commit()
    
    return redirect(url_for('cadastrar'))



@app.route('/salvar_produto', methods=['POST',])
def salvar_produto():
    # nome=request.form['nome']
    # email=request.form['email']
    # senha=request.form['senha']
    
    # jogo=Jogos.query.filter_by(nome=nome).first()
    
    # if jogo:
    #     flash('Jogo já existente')
    #     return redirect(url_for('index'))
    
    # novo_jogo=Jogos(nome=nome, categoria=categoria,console=console)
    # db.session.add(novo_jogo)
    # db.session.commit()
    
    return redirect(url_for('index'))












if __name__ == '__main__':
    app.run(debug=True)


