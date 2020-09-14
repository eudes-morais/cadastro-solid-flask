from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe Empresa -----------------------------------------------
class Produto(db.Model):
    __tablename__ = 'produto'
    idproduto = db.Column(db.Integer, primary_key=True)
    codprodutoncm = db.Column(db.String(11))
    codncm = db.Column(db.String(8))
    descricao = db.Column(db.String(150))
    quantidade = db.Column(db.Float)
    unidademedida = db.Column(db.String(12))

    # Método construtor
    def __init__(self, codprodutoncm, codncm, descricao, quantidade, unidademedida):
        self.codprodutoncm = codprodutoncm
        self.codncm = codncm
        self.descricao = descricao
        self.quantidade = quantidade
        self.unidademedida = unidademedida

# Caso seja necessário criar o BD
#db.create_all()