import psycopg

def connect():
    try:
        return psycopg.connect(
            host='localhost',
            dbname='AulaBD2', 
            user = 'postgres', 
            password = 'pedro12',
            port = '5432'
    )
    except psycopg.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")