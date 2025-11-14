import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Fofurica.10'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `leilao`;")

cursor.execute("CREATE DATABASE `leilao`;")

cursor.execute("USE `leilao`;")

# criando tabelas
TABLES = {}
TABLES['Cadastros'] = ('''
      CREATE TABLE `cadastros` (
      `id_usuario` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(255) NOT NULL,
      `cpf` char(14) NOT NULL,
      `rg` varchar(14) NOT NULL,
      `data_nascimento` date NOT NULL,
      `email` varchar(320) NOT NULL,
      `senha` varchar(255) NOT NULL,
      `cep` char(9) NOT NULL,
      `rua` varchar(255) NOT NULL,
      `bairro` varchar(255) NOT NULL,
      `complemento` varchar(255) NOT NULL,
      `pais` varchar(255) NOT NULL,
      `cidade` varchar(255) NOT NULL,
      `estado` varchar(255) NOT NULL,
      `telefone` VARCHAR(20) NOT NULL,
      
      PRIMARY KEY (`id_usuario`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Adm'] = ('''
      CREATE TABLE `adm` (
      `id_adm` int NOT NULL AUTO_INCREMENT,
      `email` varchar(320) NOT NULL,
      `senha` varchar(255) NOT NULL,
      PRIMARY KEY (`id_adm`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Produtos'] = ('''
      CREATE TABLE `produtos` (
      `id_produto` int NOT NULL AUTO_INCREMENT,
      `nome_produto` varchar(255) NOT NULL,
      `descricao_produto` text,
      `categoria_produto` varchar(100),
      `preco_produto` decimal(10,2) NOT NULL,
      `incremento_minimo` decimal(10,2) NOT NULL,
      `id_usuario` int NOT NULL,
      PRIMARY KEY (`id_produto`),
      FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`) 
            ON DELETE CASCADE
            ON UPDATE CASCADE
            
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')
      
TABLES['Lances'] = ('''
      CREATE TABLE `lances` (
      `id_lance` int NOT NULL AUTO_INCREMENT,
      `valor_lance` decimal(10,2) NOT NULL,
      `horario_lance` DATETIME DEFAULT CURRENT_TIMESTAMP,
      `id_usuario` int,
      `id_produto` int,
      PRIMARY KEY (`id_lance`),
      FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
      FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`) ON DELETE CASCADE ON UPDATE CASCADE
      
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')
      
      
TABLES['Imagens'] = ('''
      CREATE TABLE `imagens` (
      `id_imagem` int NOT NULL AUTO_INCREMENT, 
      `nome_imagem` varchar(255),
      `mimetype` varchar(100),
      `img` longblob,
      `id_usuario` int,
      `id_produto` int,
      PRIMARY KEY (`id_imagem`),
      FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
      FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`) ON DELETE CASCADE ON UPDATE CASCADE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')
      


for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios adm
usuario_sql = 'INSERT INTO adm (email, senha) VALUES (%s, %s)'
adm = [
      ("fabii@gmail.com", "1234"),
      ("biaa@gmail.com", "4321")
]
cursor.executemany(usuario_sql, adm)

cursor.execute('select * from leilao.adm')
print(' -------------  Adms:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo usuarios no cadastro
cadastros_sql = 'INSERT INTO cadastros (nome, cpf, data_nascimento, email, senha, cep, rg, rua, bairro, complemento, pais, cidade, telefone, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
cadastros = [
      (
        'Fabi', '445.678.678-98', '2009-09-09', 'fabis@gmail.com', 'aham10', 
        '12345678', '45.678.123-0', 'Rua das Flores', 'Centro', 'Casa 2', 
        'Brasil', 'São Paulo', '11987654321', 'SP'
    ),
    (
        'Maria', '998.776.675-86', '1980-09-07', 'mria@hormail.com', 'demais4445', 
        '98798798', '33.456.987-4', 'Av. Brasil', 'Jardins', 'Apto 101', 
        'Brasil', 'Rio de Janeiro', '21999887766', 'RJ'
    ),
    (
        'Julio', '098.665.445-87', '2009-12-16', 'hulio@gmail.com', 'senhazona', 
        '12312312', '12.345.678-9', 'Rua Azul', 'Vila Nova', 'Fundos', 
        'Brasil', 'Curitiba', '41988776655', 'PR'
    ),
    (
        'nana', '845.678.678-58', '2010-05-30', 'nana@gmail.com', 'numerogrande', 
        '23443223', '98.765.123-1', 'Rua Bela Vista', 'Centro', 'Bloco B', 
        'Brasil', 'Salvador', '71987654321', 'BA'
    )
      
      
]
cursor.executemany(cadastros_sql, cadastros)

cursor.execute('select * from leilao.cadastros')
print(' -------------  Usuarios:  -------------')
for cadastro in cursor.fetchall():
      print(cadastro[1])
      
#inserindo produtos na lista de produtos lá
produtos_sql = 'INSERT INTO produtos (nome_produto, categoria_produto, preco_produto, incremento_minimo, descricao_produto, id_usuario) VALUES (%s, %s, %s, %s, %s, %s)'
produtos = [
      ('caneca', 'casual', 20.99, 5.00,'descricao muitolongaaaaaaaaaaaaaa', 2),
      ('flor', 'casual', 45.99, 10.00, 'descricao mais longa aindaaaaaaaa',3)
]
cursor.executemany(produtos_sql, produtos)

cursor.execute('select * from leilao.produtos')
print(' -------------  Produtos:  -------------')
for produto in cursor.fetchall():
      print(produto[1])
      
    
#inserindo os lances
lances_sql = 'INSERT INTO lances (valor_lance, horario_lance, id_usuario, id_produto) VALUES (%s, %s, %s, %s)'
lances = [
      (21.99, '2025-10-26 14:30:00', 2, 1),
      (46.99, '2025-10-27 14:30:00', 3, 2),

]
cursor.executemany(lances_sql, lances)

cursor.execute('select * from leilao.lances')
print(' -------------  Lances:  -------------')
for lance in cursor.fetchall():
      print(lance[1])



# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()