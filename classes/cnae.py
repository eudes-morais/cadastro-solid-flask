from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe CNAE -----------------------------------------------
class Cnae(db.Model):
    __tablename__ = 'cnae'
    idcnae = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(7))
    descricao = db.Column(db.String(200))
    
    # Método construtor
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao