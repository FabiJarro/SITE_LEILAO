from leilao import db

class Cadastros(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)          
    cpf = db.Column(db.String(14), nullable=False, unique=True) 
    data_nascimento = db.Column(db.Date, nullable=False)
    email=db.Column(db.String(320), nullable=False)
    senha = db.Column(db.String(255), nullable=False)         
    cep = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Cadastro {self.nome}>'

    
class Adm(db.Model):
    id_adm= db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(320), nullable=False)
    senha=db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Adm {self.email}>'
