from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def connect():
    try:
        # Configuração do engine do SQLAlchemy
        engine = create_engine('postgresql+psycopg2://postgres:pedro12@localhost:5432/AulaBD2')
        
        # Cria e retorna uma fábrica de sessões
        Session = sessionmaker(bind=engine)
        return Session()
        
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise