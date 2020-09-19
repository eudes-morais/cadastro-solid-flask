from flask import render_template, url_for, redirect, flash, request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination
from classes.orgao import Orgao
from app import db

#-------------------------------------------------------------------------------
#----------------------------- ROTAS DA EMPRESA --------------------------------
#-------------------------------------------------------------------------------

# Utilização de BLUEPRINT (ver em: https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints)
orgao_page = Blueprint('orgao_page', __name__, template_folder='routes')

# Rota para carregar as informações digitadas ao se cadastrar um novo ORGÃO
@orgao_page.route("/cadastroorgao", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nomeorgao = request.form.get("nome")
        contato = request.form.get("contato")
        telefone1 = request.form.get("telefone1")
        telefone2 = request.form.get("telefone2")
        logradouro = request.form.get("logradouro")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        cep = str(request.form.get("cep"))
        
        # Construtor da classe ORGÃO
        orgao = Orgao(nomeorgao, contato, telefone1, telefone2, logradouro, complemento, bairro, 
                        cidade, estado, cep)
        db.session.add(orgao)
        db.session.commit()
        
        mensagem = "Orgão gravado com sucesso"
        alerta = "success"

        flash(mensagem, alerta)
        return redirect(url_for("orgao_page.listar"))

# Rota para a página que exibe a listagem de TODOS os ORGÃOS.
@orgao_page.route("/listaorgao")
def listar():
    limit = 10
    orgaos = Orgao.query.order_by(Orgao.idorgao).all()

    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(orgaos) > page * limit else len(orgaos)
    paginate = Pagination(page=page, total=len(orgaos), css_framework='bootstrap4')
    pageOrgaos = Orgao.query.order_by(Orgao.idorgao).slice(start, end)
    return render_template("listaorgao.html", orgaos = pageOrgaos, start=start + 1, end=end, pagination=paginate)

# Rota para exclusão de um ORGÃO existente
@orgao_page.route("/excluiorgao/<int:id>", methods = ['GET', 'POST'])
def excluir(id):
    orgao = Orgao.query.get(id)
    
    db.session.delete(orgao)
    db.session.commit()

    mensagem = "Orgão deletado"
    alerta = "success"

    flash(mensagem, alerta)
    return redirect(url_for("orgao_page.listar"))

# Rota para a página de alteração das informações do Órgão. 
# É importante que seja adicionado o método GET (juntamente com o método POST)
# em ROUTE para que traga as informações que serão alteradas
@orgao_page.route("/atualizarorgao/<int:id>", methods=['GET','POST'])
def atualizar(id):
    orgao = Orgao.query.get(id)
    
    if (request.method == 'POST'):
        nomeorgao = request.form.get("nome")
        contato = request.form.get("contato")
        telefone1 = request.form.get("telefone1")
        telefone2 = request.form.get("telefone2")
        logradouro = request.form.get("logradouro")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        cep = str(request.form.get("cep"))

        # Aqui pode ser criada uma validação para verificar se algo foi digitado para ser gravado no BD
        # Atualizando no BD as informações da empresa
        orgao.nomeorgao = nomeorgao
        orgao.contato = contato
        orgao.telefone1 = telefone1
        orgao.telefone2 = telefone2
        orgao.logradouro = logradouro
        orgao.complemento = complemento
        orgao.bairro = bairro
        orgao.cidade = cidade
        orgao.estado = estado
        orgao.cep = cep

        db.session.commit()

        mensagem = "Órgão atualizado"
        alerta = "info"

        flash(mensagem, alerta)
        
        return redirect(url_for("orgao_page.listar"))
    
    return render_template("atualizaorgao.html", orgao = orgao)