import datetime
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_paginate import Pagination
from flask_sqlalchemy import SQLAlchemy
from classes.funcionario import Funcionario
from classes.enderecofuncionario import EnderecoFuncionario
from classes.empresa import Empresa
from classes.estado import Estado
from app import db

#-------------------------------------------------------------------------------
#--------------------------- ROTAS DO FUNCIONÁRIO ------------------------------
#-------------------------------------------------------------------------------

# Utilização de BLUEPRINT (ver em: https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints)
funcionario_page = Blueprint('funcionario_page', __name__, template_folder='routes')
# Rota para carregar as informações digitadas na página de cadastro do FUNCIONÁRIO
@funcionario_page.route("/cadastrofuncionario", methods=['GET','POST'])
def cadastroFuncionario():
    if request.method == 'POST':
        empresafunc_id = request.form.get("empresa")
        nomefuncionario = request.form.get("nomefuncionario")
        nacionalidade = request.form.get("nacionalidade")
        cpf = str(request.form.get("cpf"))
        rg = str(request.form.get("identidade"))
        orgaoexpedidor = request.form.get("orgaoexpedidor")
        grauinstrucao = request.form.get("grauinstrucao")
        datanascimento = datetime.datetime.strptime(request.form.get("datanascimento"), '%d/%m/%Y')
        estadocivil = request.form.get("estadocivil")
        profissao = request.form.get("profissao")
        nomepai = request.form.get("nomepai")
        nomemae = request.form.get("nomemae")
        email = request.form.get("emailfuncionario")
        cargo = request.form.get("cargo")
        telefone1 = request.form.get("telefone3")
        telefone2 = request.form.get("telefone4")
        logradouro = request.form.get("logradouro1")
        complemento = request.form.get("complemento1")
        bairro = request.form.get("bairro1")
        uf = request.form.get("uf1")
        cidade = request.form.get("cidade1")
        municipio = request.form.get("municipio1")
        estado = request.form.get("estado1")
        cep = str(request.form.get("cep1"))

        # Aqui pode ser criada uma validação para verificar 
        # se algo foi digitado para ser gravado no BD
        funcionario = Funcionario(nomefuncionario, cpf, rg, orgaoexpedidor, grauinstrucao, nacionalidade,
                                    estado, municipio, datanascimento, estadocivil, profissao, nomepai,
                                    nomemae, email, cargo, telefone1, telefone2, empresafunc_id)
        db.session.add(funcionario)

        # O comando abaixo força a criação do ID no BD
        db.session.flush()

        funcionario_id = funcionario.idfuncionario
        enderecofuncionario = EnderecoFuncionario(logradouro, complemento, bairro, cidade, uf, cep, funcionario_id)

        db.session.add(enderecofuncionario)
        db.session.commit()
        
        return redirect(url_for("funcionario_page.listaFuncionarios"))

# Rota para a página que exibe uma listagem de TODOS os FUNCIONÁRIOS
@funcionario_page.route("/listafuncionarios")
def listaFuncionarios():
    limit = 10
    funcionarios = Funcionario.query.order_by(Funcionario.idfuncionario).all()
    empresas = Empresa.query.all()
    estados = Estado.query.all()
    enderecofuncionarios = EnderecoFuncionario.query.all()

    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(funcionarios) > page * limit else len(funcionarios)
    paginate = Pagination(page=page, total=len(funcionarios), css_framework='bootstrap4')
    pageFuncionarios = Funcionario.query.slice(start, end)
    return render_template("listafuncionario.html", empresas = empresas, funcionarios = pageFuncionarios,
                            enderecofuncionarios =  enderecofuncionarios, estados = estados,
                            start=start + 1, end=end, pagination=paginate)

# Rota para exclusão de um FUNCIONÁRIO
@funcionario_page.route("/excluirfuncionario/<int:id>")
def excluirFuncionario(id):
    funcionario = Funcionario.query.get(id)
    enderecofuncionario = EnderecoFuncionario.query.get(funcionario.idfuncionario)
    
    db.session.delete(enderecofuncionario)
    db.session.commit()
    
    db.session.delete(funcionario)
    db.session.commit()

    mensagem = "Funcionário excluído"
    alerta = "success"

    flash(mensagem, alerta)
    return redirect(url_for("funcionario_page.listaFuncionarios"))

# Rota para a página de edição de FUNCIONÁRIO
# É importante que seja adicionado o método GET em ROUTE para que traga as informações que serão editadas
@funcionario_page.route("/atualizarfunc/<int:id>", methods=['GET','POST'])
def atualizarFuncionario(id):
    funcionario = Funcionario.query.get(id)
    empresa = Empresa.query.all()
    idenderecofuncionario = funcionario.idfuncionario
    enderecofuncionario = EnderecoFuncionario.query.get(idenderecofuncionario)

    if (request.method == 'POST'):
        empresafunc_id = request.form.get("empresa")
        nomefuncionario = request.form.get("nomefuncionario")
        nacionalidade = request.form.get("nacionalidade")
        municipio = request.form.get("municipio")
        uf = request.form.get("uf")
        cpf = str(request.form.get("cpf"))
        rg = str(request.form.get("identidade"))
        orgaoexpedidor = request.form.get("orgaoexpedidor")
        grauinstrucao = request.form.get("grauinstrucao")
        datanascimento = datetime.datetime.strptime(request.form.get("datanascimento"), '%d/%m/%Y')
        estadocivil = request.form.get("estadocivil")
        profissao = request.form.get("profissao")
        nomepai = request.form.get("nomepai")
        nomemae = request.form.get("nomemae")
        email = request.form.get("email")
        cargo = request.form.get("cargo")
        telefone1 = request.form.get("telefone1")
        telefone2 = request.form.get("telefone2")
        logradouro = request.form.get("logradouro")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        municipio = request.form.get("municipio")
        uf = request.form.get("uf")
        estado = request.form.get("estado")
        cidade = request.form.get("cidade")
        cep = str(request.form.get("cep"))
    
        # Aqui pode ser criada uma validação para verificar se algo foi digitado para ser gravado no BD
        # Atualizando no BD as informações da empresa
        funcionario.nomefuncionario = nomefuncionario
        funcionario.nacionalidade = nacionalidade
        funcionario.cpf = cpf
        funcionario.rg = rg
        funcionario.orgaoexpedidor = orgaoexpedidor
        funcionario.nacionalidade = nacionalidade
        funcionario.estado = estado
        funcionario.municipio = municipio
        funcionario.grauintrucao = grauinstrucao
        funcionario.datanascimento = datanascimento
        funcionario.estadocivil = estadocivil
        funcionario.profissao = profissao
        funcionario.nomepai = nomepai
        funcionario.nomemae = nomemae
        funcionario.email = email
        funcionario.cargo = cargo
        funcionario.telefone1 = telefone1
        funcionario.telefone2 = telefone2
       
        # Um commit para cada tabela. Commit na tabela FUNCIONÁRIO
        db.session.commit()

        # Atualizando no BD as informações do endereço do funcionário
        enderecofuncionario.cep = cep
        enderecofuncionario.logradouro = logradouro
        enderecofuncionario.complemento = complemento
        enderecofuncionario.bairro = bairro
        enderecofuncionario.estado = uf
        enderecofuncionario.cidade = cidade

        # Commit na tabela ENDERECOEMPRESA
        db.session.commit()

        mensagem = "Funcionário atualizado"
        alerta = "info"

        flash(mensagem, alerta)
        
        return redirect(url_for("funcionario_page.listaFuncionarios"))
    
    mensagem = "Ocorreu um erro ao atualizar o Funcionário"
    alerta = "danger"
    
    return redirect(url_for("funcionario_page.listaFuncionarios"))