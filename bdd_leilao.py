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
      `data_nascimento` date NOT NULL,
      `email` varchar(320) NOT NULL,
      `senha` varchar(255) NOT NULL,
      `cep` varchar(255) NOT NULL,
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
      `categoria_produto` varchar(100),
      `preco_produto` decimal(10,2) NOT NULL,
      `incremento_minimo` decimal(10,2) NOT NULL,
      `id_usuario` int,
      PRIMARY KEY (`id_produto`),
      FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`)
      
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')
      
TABLES['Lances'] = ('''
      CREATE TABLE `lances` (
      `id_lance` int NOT NULL AUTO_INCREMENT,
      `valor_lance` decimal(10,2) NOT NULL,
      `horario_lance` datetime NOT NULL,
      `id_usuario` int,
      `id_produto` int,
      PRIMARY KEY (`id_lance`),
      FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`) ON DELETE CASCADE,
      FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`) ON DELETE CASCADE
      
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
cadastros_sql = 'INSERT INTO cadastros (nome, cpf, data_nascimento, email, senha, cep) VALUES (%s, %s, %s, %s, %s, %s)'
cadastros = [
      ('Fabi', '445678678-98', '2009-09-09', 'fabis@gmail.com', 'aham10', '1234568889'),
      ('Maria', '998776675-86', '1980-09-07', 'mria@hormail.com', 'demais4445', '098765432222'),
      ('Julio', '098665445-87', '2009-12-16', 'hulio@gmail.com', 'senhazona', '123567899'),
      ('nana', '845678678-58', '2010-05-30', 'nana@gmail.com', 'numerogrande', '5634568889')
      
      
]
cursor.executemany(cadastros_sql, cadastros)

cursor.execute('select * from leilao.cadastros')
print(' -------------  Usuarios:  -------------')
for cadastro in cursor.fetchall():
      print(cadastro[1])
      
#inserindo produtos na lista de produtos lá
produtos_sql = 'INSERT INTO produtos (nome_produto, categoria_produto, preco_produto, incremento_minimo, id_usuario) VALUES (%s, %s, %s, %s, %s)'
produtos = [
      ('caneca', 'casual', 20.99, 5.00, 2),
      ('flor', 'casual', 45.99, 10.00, 3)
]
cursor.executemany(produtos_sql, produtos)

cursor.execute('select * from leilao.produtos')
print(' -------------  Produtos:  -------------')
for produto in cursor.fetchall():
      print(produto[1])
      
    
#inserindo os lances
lances_sql = 'INSERT INTO lances (valor_lance, horario_lance, id_usuario, id_produto) VALUES (%s, %s, %s, %s)'
lances = [
      (21.99, '', 2, 1),
      (46.99, '2025-10-27 14:30:00 ', 3, 2),

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