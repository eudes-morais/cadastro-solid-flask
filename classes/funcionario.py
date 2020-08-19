from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

#-------------------------------------- Classe Funcionário -------------------------------------------
class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    idfuncionario = db.Column(db.Integer, primary_key=True)
    nomefuncionario = db.Column(db.String(150))
    cpf = db.Column(db.String(11))
    rg = db.Column(db.String(11))
    orgaoexpedidor = db.Column(db.String(11))
    grauinstrucao = db.Column(db.String(25))
    nacionalidade = db.Column(db.String(40))
    estado = db.Column(db.String(20))
    municipio = db.Column(db.String(100))
    datanascimento = db.Column(db.DateTime)
    estadocivil = db.Column(db.String(13))
    profissao = db.Column(db.String(50))
    nomepai = db.Column(db.String(150))
    nomemae = db.Column(db.String(150))
    email = db.Column(db.String(50))
    cargo = db.Column(db.String(50))
    telefone1 = db.Column(db.String(15))
    telefone2 = db.Column(db.String(15)) 
    empresafunc_id = db.Column(db.Integer, db.ForeignKey('empresa.idempresa'))
    empresasfunc = db.relationship('Empresa', backref='funcionarios', uselist=False)

    # Método construtor
    def __init__(self, nomefuncionario, cpf, rg, orgaoexpedidor, grauinstrucao, nacionalidade, estado,
                    municipio, datanascimento, estadocivil, profissao, nomepai, nomemae, email, cargo,
                    telefone1, telefone2, empresafunc_id):
        self.nomefuncionario = nomefuncionario
        self.cpf = cpf
        self.rg = rg
        self.orgaoexpedidor = orgaoexpedidor
        self.grauinstrucao = grauinstrucao
        self.nacionalidade = nacionalidade
        self.estado = estado
        self.municipio = municipio
        self.datanascimento = datanascimento
        self.estadocivil = estadocivil
        self.profissao = profissao
        self.nomepai = nomepai
        self.nomemae = nomemae
        self.email = email
        self.cargo = cargo
        self.telefone1 = telefone1
        self.telefone2 = telefone2
        self.empresafunc_id = empresafunc_id