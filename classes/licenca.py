from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

#-------------------------------------- Classe Endereço -----------------------------------------------
class Licenca(db.Model):
    __tablename__ = 'licenca'
    idlicenca = db.Column(db.Integer, primary_key=True)
    datainicial = db.Column(db.DateTime)
    datafinal = db.Column(db.DateTime)
    valor = db.Column(db.Float)
    orgao_id = db.Column(db.Integer, db.ForeignKey('orgao.idorgao'))
    orgaos = db.relationship('Orgao', backref='licencas')
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.idempresa'))
    empresas = db.relationship('Empresa', backref='licencas')
    # If you would want to have a one-to-one relationship you can pass uselist=False to relationship()
    
    # Método construtor
    def __init__(self, datainicial, datafinal, valor, orgao_id, empresa_id):
        self.datainicial = datainicial
        self.datafinal = datafinal
        self.valor = valor
        self.orgao_id = orgao_id
        self.empresa_id = empresa_id