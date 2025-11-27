
from leilao import app
import re    
import hashlib
from models import Cadastros, Adm, Produtos, Lances, Imagens
from leilao import db


def hashSenha(senha):
    texto_bytes = senha.encode('utf-8')
    hash_sha256 = hashlib.sha256(texto_bytes)
    return hash_sha256.hexdigest()

        
class UsuarioForm():
    
    def __init__(self, form):
        self.form = form
        self.nome = form.get('nome')
        self.cpf = form.get('cpf')
        self.rg= form.get('rg')
        self.numero_casa= form.get('numero_casa')
        self.data_nascimento = form.get('data_nascimento')
        self.senha = form.get('senha')
        self.email = form.get('email')
        self.cep = form.get('cep')
        self.rua = form.get('rua')
        self.bairro = form.get('bairro')
        self.complemento= form.get('complemento')
        self.pais= form.get('pais')
        self.cidade= form.get('cidade')
        self.estado= form.get('estado')
        self.telefone = form.get('telefone')
        
        
    
    def validar_cpf(self):
        padrao = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
        return bool(re.match(padrao, self.cpf))
    
    def validar(self):
        # print('XPTO', len(self.nome), len(self.nome) < 15 or len(self.nome) > 255)
        if len(self.nome) < 1 or len(self.nome) > 255:
            raise ValueError('O valor do nome deve ser entre 1 e 255 caracteres')
        
        if not self.validar_cpf():
            raise ValueError('CPF inválido!')
        
        # if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', self.data_nascimento):  
        #     raise ValueError('A data de nascimento deve estar no formato AAAA-MM-DD.')
        # Aceita DD/MM/YYYY e converte para YYYY-MM-DD
        if re.fullmatch(r'\d{2}/\d{2}/\d{4}', self.data_nascimento):
            dia, mes, ano = self.data_nascimento.split('/')
            self.data_nascimento = f"{ano}-{mes}-{dia}"  # converte para AAAA-MM-DD
        else:
            raise ValueError('A data de nascimento deve estar no formato DD/MM/AAAA.')

        
        if '@' not in self.email or '.' not in self.email:
            raise ValueError('O email informado é inválido.')

        # if not re.fullmatch(r'\d{8}', self.cep):
        #     raise ValueError('O CEP deve conter exatamente 8 dígitos numéricos.')
        
        if len(self.senha) < 1 or len(self.senha) > 255:
            raise ValueError('O valor da senha deve ser entre 1 e 255 caracteres')
        
        cep_limpo = re.sub(r'\D', '', self.cep)

        if not re.fullmatch(r'\d{8}', cep_limpo):
            raise ValueError('O CEP deve conter exatamente 8 dígitos numéricos.')

        self.cep = cep_limpo
        
        return True


class ProdutoForm():
    
    def __init__(self, form):
        self.form = form
        self.nome_produto = form.get('nome_produto')
        self.categoria_produto = form.get('categoria_produto')
        self.descricao_produto = form.get('descricao_produto')
        self.preco_produto = form.get('preco_produto')
        self.incremento_minimo = form.get('incremento_minimo')
        self.data_final= form.get('data_final')
        
        
    
    def validarProduto(self):
        if len(self.nome_produto) < 1 or len(self.nome_produto) > 255:
            raise ValueError('O valor do nome do produto deve ser entre 1 e 255 caracteres')

        if len(self.descricao_produto) < 1:
            raise ValueError('A descrição do produto é obrigatória')
        
        if self.preco_produto.isalpha():
            raise ValueError('Digite um valor válido')
        
        if self.incremento_minimo.isalpha():
            raise ValueError('Digite um valor válido')
        return True
    
    
    
def finalizar_leilao(id_produto):
    with app.app_context(): 
        produto = Produtos.query.get(id_produto)

        if not produto:
            print("Produto não encontrado")
            return

        # Já está finalizado?
        # if produto.status == "finalizado":
        #     return

        print(f"Finalizando leilão do produto {produto.nome_produto}")

        ultimo_lance = (
            Lances.query.filter_by(id_produto=id_produto)
            .order_by(Lances.valor_lance.desc(), Lances.horario_lance.desc())
            .first()
        )

        if ultimo_lance:
            produto.id_ganhador = ultimo_lance.id_usuario
            produto.lance_final = ultimo_lance.valor_lance
            print(f"Ganhador: usuario {ultimo_lance.id_usuario}")
        else:
            print("Nenhum lance foi feito")

        # produto.status = "finalizado"
        db.session.commit()
        print("Leilão finalizado com sucesso!")
