from flask_sqlalchemy import SQLAlchemy
from app import db

#-------------------------------------- Classe Endereço -----------------------------------------------
class EnderecoEmpresa(db.Model):
    __tablename__ = 'enderecoempresa'
    idenderecoemp = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String(150))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(20))
    cep = db.Column(db.String(8))
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.idempresa'))
    empresas = db.relationship('Empresa', backref='enderecos', uselist=False)
    
    # Método construtor
    def __init__(self, logradouro, complemento, bairro, cidade, estado, cep, empresa_id):
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.empresa_id = empresa_id