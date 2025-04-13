import psycopg

def connect():
    try:
        return psycopg.connect(
            host='localhost',
            dbname='northwind', 
            user = 'postgres', 
            password = '1234',
            port = '5432'
    )
    except psycopg.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        