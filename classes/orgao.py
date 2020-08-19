from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe Empresa -----------------------------------------------
class Orgao(db.Model):
    __tablename__ = 'orgaoresponsavel'
    idorgao = db.Column(db.Integer, primary_key=True)
    nomeorgao = db.Column(db.String(150))
    contato = db.Column(db.String(50))
    telefone1 = db.Column(db.String(15))
    telefone2 = db.Column(db.String(15))
    logradouro = db.Column(db.String(150))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(20))
    cep = db.Column(db.String(8))


    # Método construtor
    def __init__(self, nomeorgao, contato, telefone1, telefone2, logradouro, complemento, bairro,
                cidade, estado, cep):
        self.nomeorgao = nomeorgao
        self.contato = contato
        self.telefone1 = telefone1
        self.telefone2 = telefone2
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep