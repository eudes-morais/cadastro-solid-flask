from flask import render_template, url_for, redirect, flash, request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination
from classes.produto import Produto
from classes.atividade import Atividade
from classes.licenca import Licenca
from classes.empresa import Empresa
from app import db

#-------------------------------------------------------------------------------
#-------------------- ROTAS LICENÇAS/ATIVIDADES/PRODUTOS -----------------------
#-------------------------------------------------------------------------------

# Utilização de BLUEPRINT (ver em: https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints)
lap_page = Blueprint('lap_page', __name__, template_folder='routes')

# Como se trata de uma DUALLISTBOX, não existe as funções
# para cadastrar e excluir PRODUTOS ou ATIVIDADES

# Rota para a página de ATIVIDADES e PRODUTOS que estão vinculadas a LICENÇA
# É importante que seja adicionado o método GET (juntamente com o método POST)
# em ROUTE para que traga as informações que serão alteradas
@lap_page.route("/lap/<int:id>", methods=['GET','POST'])
def listalap(id):
    licenca = Licenca.query.get(id)
    produtos = Produto.query.all()
    atividades = Atividade.query.all()
    empresa = Empresa.query.get(licenca.empresa_id)
    
    return render_template("listalap.html", empresa = empresa, licenca = licenca,
                            produtos = produtos, atividades = atividades)

# Rota para alteração de ATIVIDADES e/ou PRODUTOS
@lap_page.route("/atualizalap/<int:id>", methods=['GET','POST'])
def atualizalap(id):
    licenca = Licenca.query.get(id)
    produtos = Produto.query.all()
    atividades = Atividade.query.all()

    if (request.method == 'POST'):
        listaatividades = []
        listaprodutos = []
        # Conversão de uma lista de string para uma lista de inteiro
        # Extraído de https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
        listaatividades = [int(i) for i in request.form.getlist("duallistbox_atividades[]")]
        listaprodutos = [int(i) for i in request.form.getlist("duallistbox_produtos[]")]
        empresa_id = request.form.get("empresaid")

        licenca.atividade_id = listaatividades
        licenca.produto_id = listaprodutos

        # Commit na tabela LICENÇA
        db.session.commit()

        mensagem = "Atividades/Produtos atualizados"
        alerta = "info"

        flash(mensagem, alerta)
        
        return redirect(url_for("licenca_page.listarlicencas", id=empresa_id))
    
    return render_template("listalap.html", licenca = licenca, produtos = produtos, atividades = atividades)