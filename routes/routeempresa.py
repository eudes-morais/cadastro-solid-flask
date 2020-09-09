from flask import render_template, url_for, redirect, flash, request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination
# from classes.cnae import *
from classes.empresa import Empresa
from classes.enderecoempresa import EnderecoEmpresa
import classes.cnae
from app import db

#-------------------------------------------------------------------------------
#----------------------------- ROTAS DA EMPRESA --------------------------------
#-------------------------------------------------------------------------------

# Utilização de BLUEPRINT (ver em: https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints)
empresa_page = Blueprint('empresa_page', __name__, template_folder='routes')

# Rota para carregar as informações digitadas ao se cadastrar uma nova EMPRESA
@empresa_page.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        numeropasta = request.form.get("numeropasta")
        razaoSocial = request.form.get("razaosocial")
        inscEst = request.form.get("inscricaoestadual")
        cnpj = request.form.get("cnpj")
        cxPostal = request.form.get("caixapostal")
        email = request.form.get("email")
        cnae_id = str(request.form.get("cnae"))
        telefone1 = request.form.get("telefone1")
        telefone2 = request.form.get("telefone2")
        logradouro = request.form.get("logradouro")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        cep = str(request.form.get("cep"))
        
        # Construtor da classe EMPRESA
        empresa = Empresa(numeropasta, razaoSocial, inscEst, cnpj, cxPostal, email, cnae_id, telefone1, telefone2)
        db.session.add(empresa)
        # O comando abaixo força a criação do ID no BD
        db.session.flush()

        # 'Captura' o ID da empresa para ser adicionado na tabela ENDERECOEMPRESA
        empresa_id = empresa.idempresa

        # Construtor da classe ENDERECOEMPRESA
        enderecoempresa = EnderecoEmpresa(logradouro, complemento, bairro, cidade, estado, cep, empresa_id=empresa.idempresa)
        db.session.add(enderecoempresa)
        db.session.commit()
        
        mensagem = "Empresa gravada com sucesso"
        alerta = "success"

        flash(mensagem, alerta)
        return redirect(url_for("empresa_page.listar"))

# Rota para a página que exibe a listagem com as EMPRESAS.
# Nessa listagem ocorre a PAGINAÇÃO das empresas.
# Ou seja, elas são exibidas de 10 em 10 empresas.
@empresa_page.route("/lista")
def listar():
    limit = 10
    empresas = Empresa.query.order_by(Empresa.numeropasta).all()
    cnae = classes.cnae.Cnae.query.all()
    enderecoempresa = EnderecoEmpresa.query.all()

    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(empresas) > page * limit else len(empresas)
    paginate = Pagination(page=page, total=len(empresas), css_framework='bootstrap4')
    pageEmpresas = Empresa.query.order_by(Empresa.numeropasta).slice(start, end)
    # pagination = Pagination(page=page, total=len(empresas), per_page=per_page, css_framework='bootstrap4')
    return render_template("lista.html", empresas = pageEmpresas, cnae = cnae, start=start + 1, end=end,
                            enderecoempresa = enderecoempresa, pagination=paginate)

# Rota para exclusão de uma EMPRESA existente
@empresa_page.route("/excluir/<int:id>", methods = ['GET', 'POST'])
def excluir(id):
    empresa = Empresa.query.get(id)
    idenderecoempresa = empresa.idempresa
    enderecoempresa = EnderecoEmpresa.query.get(idenderecoempresa)
    
    db.session.delete(enderecoempresa)
    db.session.commit()
    
    db.session.delete(empresa)
    db.session.commit()

    mensagem = "Empresa deletada"
    alerta = "success"

    flash(mensagem, alerta)
    return redirect(url_for("empresa_page.listar"))

# Rota para a página de alteração do cadastro da EMPRESA. 
# É importante que seja adicionado o método GET (juntamente com o método POST)
# em ROUTE para que traga as informações que serão alteradas
@empresa_page.route("/atualizar/<int:id>", methods=['GET','POST'])
def atualizar(id):
    cnae = classes.cnae.Cnae.query.all()
    empresa = Empresa.query.get(id)
    idenderecoempresa = empresa.idempresa
    enderecoempresa = EnderecoEmpresa.query.get(idenderecoempresa)

    if (request.method == 'POST'):
        numeropasta = request.form.get("numeropasta")
        razaoSocial = request.form.get("razaosocial")
        inscestadual = request.form.get("inscricaoestadual")
        cnpj = request.form.get("cnpj")
        cxPostal = request.form.get("caixapostal")
        email = request.form.get("email")
        cnae = request.form.get("cnae")
        telefone1 = request.form.get("telefone1")
        telefone2 = request.form.get("telefone2")
        cep = request.form.get("cep")
        logradouro = request.form.get("logradouro")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        estado = request.form.get("estado")
        cidade = request.form.get("cidade")

        # Aqui pode ser criada uma validação para verificar se algo foi digitado para ser gravado no BD
        # Atualizando no BD as informações da empresa
        empresa.numeropasta = numeropasta
        empresa.razaosocial = razaoSocial
        empresa.inscricaoestadual = inscestadual
        empresa.cnpj = cnpj
        empresa.caixapostal = cxPostal
        empresa.email = email
        empresa.cnae_id = cnae
        empresa.telefone1 = telefone1
        empresa.telefone2 = telefone2

        # Um commit para cada tabela. Commit na tabela EMPRESA
        db.session.commit()

        # Atualizando no BD as informações do endereço da empresa
        enderecoempresa.cep = cep
        enderecoempresa.logradouro = logradouro
        enderecoempresa.complemento = complemento
        enderecoempresa.bairro = bairro
        enderecoempresa.estado = estado
        enderecoempresa.cidade = cidade

        # Commit na tabela ENDERECOEMPRESA
        db.session.commit()

        mensagem = "Empresa atualizada"
        alerta = "info"

        flash(mensagem, alerta)
        
        return redirect(url_for("empresa_page.listar"))
        # return render_template("lista.html")
    
    return render_template("atualizaempresa.html", empresa = empresa, cnae = cnae, enderecoempresa = enderecoempresa)