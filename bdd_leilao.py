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

cursor.execute('DROP DATABASE IF EXISTS `leilao`;')

arquivos = ['/home/fabiana/Desktop/SITE_LEILAO/bd/01_modelo_fisico.sql',
            '/home/fabiana/Desktop/SITE_LEILAO/bd/02_insercoes_basicas.sql']

for arquivo in arquivos:
      with open(arquivo, 'r') as f:
            sql_script = f.read()
      print(sql_script)      
      statements = sql_script.split(';')
      for statement in statements:
            if statement.strip():
                  cursor.execute(statement)

cursor.execute('select * from leilao.adm')
print(' -------------  Adms:  -------------')
for user in cursor.fetchall():
    print(user[1])

cursor.execute('select * from leilao.cadastros')
print(' -------------  Usuarios:  -------------')
for cadastro in cursor.fetchall():
      print(cadastro[1])

cursor.execute('select * from leilao.produtos')
print(' -------------  Produtos:  -------------')
for produto in cursor.fetchall():
      print(produto[1])

cursor.execute('select * from leilao.lances')
print(' -------------  Lances:  -------------')
for lance in cursor.fetchall():
      print(lance[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()