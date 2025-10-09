
SECRET_KEY ='toddy'

SGBD='mysql+mysqlconnector'
usuario='root'
senha='Fofurica.10'
servidor='localhost'
database='leilao'
        
SQLALCHEMY_DATABASE_URI= f'{SGBD}://{usuario}:{senha}@{servidor}/{database}'

     