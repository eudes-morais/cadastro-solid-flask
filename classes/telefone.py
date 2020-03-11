from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe Telefone -------------------------------------------
class Telefone(db.Model):
    __tablename__ = 'telefone'
    idtelefone = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.Integer)
    numero = db.Column(db.Integer)
    empresa = db.Column(db.Integer)
    funcionario = db.Column(db.Integer)
    orgao = db.Column(db.Integer)
    
    # Método construtor
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao