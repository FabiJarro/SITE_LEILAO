
from leilao import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email
import re    

# class FormularioUsuario(FlaskForm):
#     nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=255)])
#     cpf = StringField('CPF', [validators.DataRequired(), validators.Length(min=1, max=14)])
#     data_nascimento = StringField('Data de nascimento', [DataRequired()])
#     email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=320)])
#     senha = StringField('Senha', [validators.DataRequired(), validators.Length(min=1, max=255)])
#     cep = StringField('CEP', [validators.DataRequired(), validators.Length(min=1, max=255)])
#     salvar = SubmitField('Salvar')
    
#     def hello(self):
#         print('hello')
        
class UsuarioForm():
    
    def __init__(self, form):
        self.form = form
        self.nome = form.get('nome')
        self.cpf = form.get('cpf')
        self.data_nascimento = form.get('data_nascimento')
        self.senha = form.get('senha')
        self.email = form.get('email')
        self.cep = form.get('cep')
        
    
    def validar(self):
        # print('XPTO', len(self.nome), len(self.nome) < 15 or len(self.nome) > 255)
        if len(self.nome) < 1 or len(self.nome) > 255:
            raise ValueError('O valor do nome deve ser entre 1 e 255 caracteres')
        
        if not re.fullmatch(r'\d{11}', self.cpf):
            raise ValueError('O CPF deve conter exatamente 11 dígitos numéricos.')
        
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', self.data_nascimento):  # formato do input type="date"
            raise ValueError('A data de nascimento deve estar no formato AAAA-MM-DD.')
        
        
        if '@' not in self.email or '.' not in self.email:
            raise ValueError('O email informado é inválido.')

        if not re.fullmatch(r'\d{8}', self.cep):
            raise ValueError('O CEP deve conter exatamente 8 dígitos numéricos.')
        
        if len(self.senha) < 1 or len(self.senha) > 255:
            raise ValueError('O valor da senha deve ser entre 1 e 255 caracteres')
        
        return True


class FormularioProduto(FlaskForm):
    nome_produto=('Nome do produto', [validators.DataRequired(), validators.Length(min=1, max=255)])
    descricao_produto=('Descrição do produto', [validators.DataRequired(), validators.Length(min=1, max=4000)])
    categoria_produto=('Categoria', [validators.DataRequired(), validators.Length(min=1, max=100)])
    preco_produto=('preço inicial', [validators.DataRequired(), validators.Length(min=1, max=100)])
    incremento_minimo=('incremento minimo', [validators.DataRequired(), validators.Length(min=1, max=255)])


# class UsuarioForm():
        
#     def __init__(self, form):
#         self.form = form
#         self.nome = form.get('nome')
#         self.cpf = form.get('cpf')
#         self.email = form.get('email')
#         self.cep = form.get('cep')
#         self.data_nascimento = form.get('data_nascimento')
    
