from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe CNAE -----------------------------------------------
class Estado(db.Model):
    __tablename__ = 'estado'
    idestado = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer)
    sigla = db.Column(db.String(2))
    nome = db.Column(db.String(20))
    
    # Método construtor
    def __init__(self, codigo, sigla, nome):
        self.codigo = codigo
        self.sigla = sigla
        self.nome = nome