from datetime import datetime
from flask import render_template, url_for, redirect, flash, request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination
from classes.empresa import Empresa
from classes.orgao import Orgao
from classes.licenca import Licenca
from app import db

#-------------------------------------------------------------------------------
#------------------------------ ROTAS LICENÇAS ---------------------------------
#-------------------------------------------------------------------------------

# Utilização de BLUEPRINT (ver em: https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints)
licenca_page = Blueprint('licenca_page', __name__, template_folder='routes')

# Rota para carregar as informações digitadas ao se cadastrar uma nova EMPRESA
@licenca_page.route("/cadastrolicenca", methods=['GET', 'POST'])
def cadastrolicenca():
    if request.method == 'POST':
        datainicial = datetime.strptime(request.form.get("datainicial"), '%d/%m/%Y')
        datafinal = datetime.strptime(request.form.get("datafinal"),'%d/%m/%Y')
        valorlicenca = request.form.get("valorlicenca")
        # Transformando o valor para FLOAT universal
        valorlicenca = str(valorlicenca).replace(',','.')
        orgao_id = request.form.get("orgaoresponsavel")
        empresa_id = request.form.get("empresaid")
        # Os atributos abaixo só serão utilizados depois
        produto_id = []
        atividade_id = []
        
        # Construtor da classe LICENÇA
        licenca = Licenca(datainicial, datafinal, valorlicenca, orgao_id, empresa_id, produto_id, atividade_id)
        db.session.add(licenca)
        db.session.commit()
        
        mensagem = "Licença gravada com sucesso"
        alerta = "success"

        flash(mensagem, alerta)
        return redirect(url_for('licenca_page.listarlicencas', id = empresa_id))

# Rota para a página de LICENÇAS que a empresa tem cadastradas.
# É importante que seja adicionado o método GET (juntamente com o método POST)
# em ROUTE para que traga as informações que serão alteradas
@licenca_page.route("/licencas/<int:id>", methods=['GET','POST'])
def listarlicencas(id):
    limit = 10
    empresa = Empresa.query.get(id)
    idempresa = empresa.idempresa
    orgaos = Orgao.query.all()
    licencas = Licenca.query.filter(Licenca.empresa_id == idempresa).all()
    
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(licencas) > page * limit else len(licencas)
    paginate = Pagination(page=page, total=len(licencas), css_framework='bootstrap4')
    pageLicencas = Licenca.query.order_by(Licenca.orgao_id).slice(start, end)
    return render_template("listalicenca.html", empresa = empresa, orgaos = orgaos, start=start + 1, end=end,
                            licencas = licencas, pagination=paginate)

# Rota para exclusão de uma LICENÇA existente
@licenca_page.route("/excluirlicenca/<int:id>", methods = ['GET', 'POST'])
def excluirlicenca(id):
    licenca = Licenca.query.get(id)
    empresa_id = licenca.empresa_id
    
    db.session.delete(licenca)
    db.session.commit()
    
    mensagem = "Licença deletada"
    alerta = "success"

    flash(mensagem, alerta)
    return redirect(url_for("licenca_page.listarlicencas", id = empresa_id))

# Rota para a página de alteração do cadastro da EMPRESA. 
# É importante que seja adicionado o método GET (juntamente com o método POST)
# em ROUTE para que traga as informações que serão alteradas
@licenca_page.route("/atualizarlicenca/<int:id>", methods=['GET','POST'])
def atualizarlicenca(id):
    licenca = Licenca.query.get(id)
    empresa = Empresa.query.get(licenca.empresa_id)
    orgaos = Orgao.query.all()
    
    if (request.method == 'POST'):
        # Convertendo 
        datainicial = datetime.strptime(request.form.get("datainicial"), '%d/%m/%Y')
        datafinal = datetime.strptime(request.form.get("datafinal"),'%d/%m/%Y')
        valorlicenca = request.form.get("valorlicenca")
        # Convertendo o valor para FLOAT universal
        valorlicenca = str(valorlicenca).replace(',','.')
        orgao_id = request.form.get("orgaoresponsavel")
       
        # Atualizando no BD as informações da LICENÇA (exceto as ATIVIDADES, EMPRESAS e os PRODUTOS)
        licenca.datainicial = datainicial
        licenca.datafinal = datafinal
        licenca.valorlicenca = valorlicenca
        licenca.orgao_id = orgao_id
        
        # Commit na tabela LICENÇA
        db.session.commit()

        mensagem = "Licença atualizada"
        alerta = "info"

        flash(mensagem, alerta)
        
        return redirect(url_for("licenca_page.listarlicencas"))
    
    return render_template("atualizalicenca.html", licenca = licenca, empresa = empresa, orgaos = orgaos)