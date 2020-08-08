from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe Empresa -----------------------------------------------
class Empresa(db.Model):
    __tablename__ = 'empresa'
    idempresa = db.Column(db.Integer, primary_key=True)
    numeropasta = db.Column(db.Integer)
    razaosocial = db.Column(db.String(150))
    inscricaoestadual = db.Column(db.String(15))
    cnpj = db.Column(db.String(14))
    caixapostal = db.Column(db.String(10))
    email = db.Column(db.String(50))
    cnae_id = db.Column(db.Integer)
    telefone1 = db.Column(db.String(15))
    telefone2 = db.Column(db.String(15))

    # Método construtor
    def __init__(self, numeropasta, razaosocial, inscricaoestadual, cnpj, caixapostal, email, cnae_id, telefone1, telefone2):
        self.numeropasta = numeropasta
        self.razaosocial = razaosocial
        self.inscricaoestadual = inscricaoestadual
        self.cnpj = cnpj
        self.caixapostal = caixapostal
        self.email = email
        self.cnae_id = cnae_id
        self.telefone1 = telefone1
        self.telefone2 = telefone2

# Caso seja necessário criar o BD
#db.create_all()