from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

#-------------------------------------- Classe Endereço -----------------------------------------------
class Licenca(db.Model):
    __tablename__ = 'licenca'
    idlicenca = db.Column(db.Integer, primary_key=True)
    datainicial = db.Column(db.DateTime)
    datafinal = db.Column(db.DateTime)
    valorlicenca = db.Column(db.Float)
    orgao_id = db.Column(db.Integer, db.ForeignKey('orgaoresponsavel.idorgao'))
    orgaos = db.relationship('Orgao', backref='licenca')
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.idempresa'))
    empresas = db.relationship('Empresa', backref='licenca')
    # If you would want to have a one-to-one relationship you can pass uselist=False to relationship()
    
    # Método construtor
    def __init__(self, datainicial, datafinal, valorlicenca, orgao_id, empresa_id):
        self.datainicial = datainicial
        self.datafinal = datafinal
        self.valorlicenca = valorlicenca
        self.orgao_id = orgao_id
        self.empresa_id = empresa_id