
from leilao import app
import re    


        
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


class ProdutoForm():
    
    def __init__(self, form):
        self.form = form
        self.nome_produto = form.get('nome_produto')
        self.categoria_produto = form.get('categoria_produto')
        self.descricao_produto = form.get('descricao_produto')
        self.preco_produto = form.get('preco_produto')
        self.incremento_minimo = form.get('incremento_minimo')
        
    
    def validarProduto(self):
        if len(self.nome_produto) < 1 or len(self.nome_produto) > 255:
            raise ValueError('O valor do nome do produto deve ser entre 1 e 255 caracteres')
        
        if len(self.categoria_produto) < 1 or len(self.categoria_produto) > 100:
            raise ValueError('O valor da categoria do produto deve ser entre 1 e 100 caracteres')

        if len(self.descricao_produto) < 1:
            raise ValueError('A descrição do produto é obrigatória')
        
        if self.preco_produto.isalpha():
            raise ValueError('Digite um valor válido')
        
        if self.incremento_minimo.isalpha():
            raise ValueError('Digite um valor válido')
        return True