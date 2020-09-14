from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe Atividade --------------------------------------------
class Atividade(db.Model):
    __tablename__ = 'atividade'
    idatividade = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150))

    # Método construtor
    def __init__(self, descricao):
        self.descricao = descricao

# Caso seja necessário criar o BD
#db.create_all()