from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from app import db

#-------------------------------------- Classe Endereço -----------------------------------------------
class Licenca(db.Model):
    __tablename__ = 'licenca'
    idlicenca = db.Column(db.Integer, primary_key=True)
    numerolicenca = db.Column(db.String(20))
    datainicial = db.Column(db.DateTime)
    datafinal = db.Column(db.DateTime)
    valorlicenca = db.Column(db.Float)
    orgao_id = db.Column(db.Integer, db.ForeignKey('orgaoresponsavel.idorgao'))
    orgaos = db.relationship('Orgao', backref='licenca')
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.idempresa'))
    empresas = db.relationship('Empresa', backref='licenca')
    produto_id = db.Column(ARRAY(db.Integer))
    atividade_id = db.Column(ARRAY(db.Integer))
    # If you would want to have a one-to-one relationship you can pass uselist=False to relationship()
    
    # Método construtor
    def __init__(self, numerolicenca, datainicial, datafinal, valorlicenca, orgao_id, empresa_id, produto_id, atividade_id):
        self.numerolicenca = numerolicenca
        self.datainicial = datainicial
        self.datafinal = datafinal
        self.valorlicenca = valorlicenca
        self.orgao_id = orgao_id
        self.empresa_id = empresa_id
        self.produto_id = produto_id
        self.atividade_id = atividade_id