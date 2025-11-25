from leilao import db
from datetime import datetime, timezone
# from sqlalchemy import Enum



class Cadastros(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)          
    cpf = db.Column(db.String(14), nullable=False, unique=True) 
    rg= db.Column(db.String(14), nullable=False, unique=True) 
    data_nascimento = db.Column(db.Date, nullable=False)
    email=db.Column(db.String(320), nullable=False)
    senha = db.Column(db.String(255), nullable=False)         
    cep = db.Column(db.String(9), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    bairro= db.Column(db.String(255), nullable=False)
    complemento = db.Column(db.String(255), nullable=False)
    pais= db.Column(db.String(255), nullable=False)
    cidade= db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f'<Cadastro {self.nome}>'

    
class Adm(db.Model):
    id_adm= db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(320), nullable=False)
    senha=db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Adm {self.email}>'

class Produtos(db.Model):
    __tablename__='produtos'
    
    id_produto=db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto=db.Column(db.String(255), nullable=False)
    categoria_produto=db.Column(db.String(255), nullable=False)
    data_final = db.Column(db.DateTime, nullable=False)
    preco_produto=db.Column(db.Float(255), nullable=False)
    incremento_minimo=db.Column(db.Float(255), nullable=False)
    descricao_produto = db.Column(db.Text, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('cadastros.id_usuario'))
    imagens = db.relationship('Imagens', backref='produto', lazy=True)

    usuario = db.relationship('Cadastros', foreign_keys=[id_usuario])
    
    
    def __repr__(self):
        return f'<Produto {self.nome_produto}>'

class Lances(db.Model):
    __tablename__ = 'lances'

    id_lance = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_lance = db.Column(db.Numeric(10, 2), nullable=False)
    horario_lance = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('cadastros.id_usuario', ondelete='CASCADE'))
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto', ondelete='CASCADE'))

    usuario = db.relationship('Cadastros', backref='lances', lazy=True)
    produto = db.relationship('Produtos', backref='lances', lazy=True)

    def __repr__(self):
        return f'<Lance {self.valor_lance:.2f} - Usuario {self.id_usuario}>'
    
class Imagens(db.Model):
    id_imagem= db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_imagem=db.Column(db.String(255), nullable=False)
    mimetype = db.Column(db.Text)
    img = db.Column(db.LargeBinary)
    id_usuario = db.Column(db.Integer, db.ForeignKey('cadastros.id_usuario', ondelete='CASCADE'))
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto', ondelete='CASCADE'))
    
    def __repr__(self):
        return f'<Imagens {self.nome_imagem}>'