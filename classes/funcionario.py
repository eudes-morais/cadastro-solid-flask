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
    # datanascimento = db.Column(db.String(10))
    datanascimento = db.Column(db.DateTime)
    estadocivil = db.Column(db.String(10))
    profissao = db.Column(db.String(50))
    nomepai = db.Column(db.String(150))
    nomemae = db.Column(db.String(150))
    email = db.Column(db.String(50))
    cargo = db.Column(db.String(50))
    empresafunc_id = db.Column(db.Integer, db.ForeignKey('empresa.idempresa'))
    empresasfunc = db.relationship('Empresa', backref='funcionarios', uselist=False)

    # Método construtor
    def __init__(self, nomefuncionario, cpf, rg, orgaoexpedidor, grauinstrucao, nacionalidade, datanascimento, estadocivil, profissao, nomepai, nomemae, email, cargo, empresafunc_id):
        self.nomefuncionario = nomefuncionario
        self.cpf = cpf
        self.rg = rg
        self.orgaoexpedidor = orgaoexpedidor
        self.grauinstrucao = grauinstrucao
        self.nacionalidade = nacionalidade
        self.datanascimento = datanascimento
        self.estadocivil = estadocivil
        self.profissao = profissao
        self.nomepai = nomepai
        self.nomemae = nomemae
        self.email = email
        self.cargo = cargo
        self.empresafunc_id = empresafunc_id