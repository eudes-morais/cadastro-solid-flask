import os
import psycopg2
import datetime
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://solid:solid@172.17.0.1:5432/solid"
db = SQLAlchemy(app)

# Os IMPORTS abaixo devem ficar depois do 'db = SQLAlchemy(app)', 
# para que as classes possam ser iniciadas corretamente.
#----------------------------------- IMPORTS -----------------------------------
from classes.cnae import *
from classes.empresa import *
from classes.enderecoempresa import *
from classes.enderecofuncionario import *
from classes.funcionario import *

#-------------------------------------------------------------------------------
#------------------------- Trabalhando com as rotas ----------------------------
#-------------------------------------------------------------------------------

# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

#-------------------------------------------------------------------------------
#----------------------------- ROTAS DA EMPRESA --------------------------------
#-------------------------------------------------------------------------------

# Rota para a página de cadastro da EMPRESA
@app.route("/cadastrar")
def cadastrar():
    cnae = Cnae.query.all()
    return render_template("cadastro.html", cnae = cnae)
    # return render_template("cadastro.html")

# Rota para carregar as informações digitadas na página de cadastro da EMPRESA
@app.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == 'POST':
        mensagem = ''
        alerta = ''

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
        empresa = Empresa(razaoSocial, inscEst, cnpj, cxPostal, email, cnae_id, telefone1, telefone2)
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
        alerta = "sucess"

        flash(mensagem, alerta)
        return redirect(url_for("listar"))
    # Caso não sejapossível gravar
    mensagem = "Ocorreu uma erro ao gravar a Empresa"
    alerta = "danger"

    flash(mensagem, alerta)
    return redirect(url_for("listar"))
    

# Rota para a página que exibe uma listagem das EMPRESAS
@app.route("/lista")
def listar():
    empresas = Empresa.query.order_by(Empresa.idempresa).all()
    cnae = Cnae.query.all()
    enderecoempresa = EnderecoEmpresa.query.all()
    return render_template("lista.html", empresas = empresas, cnae = cnae, enderecoempresa = enderecoempresa)

# Rota para exclusão de uma EMPRESA existente
@app.route("/excluir/<int:id>")
def excluir(id):
    empresa = Empresa.query.get(id)
    enderecoempresa = EnderecoEmpresa.query.get(empresa.idempresa)
    
    db.session.delete(enderecoempresa)
    db.session.commit()
    
    db.session.delete(empresa)
    db.session.commit()

    mensagem = "Empresa deletada"
    alerta = "sucess"

    flash(mensagem, alerta)
   
    return redirect(url_for("listar"))

# Rota para a página de alteração do cadastro da EMPRESA. 
# É importante que seja adicionado o método GET em ROUTE para que traga as informações que serão alteradas
@app.route("/atualizar/<int:id>", methods=['GET','POST'])
def atualizar(id):
    cnae = Cnae.query.all()
    empresa = Empresa.query.get(id)
    idenderecoempresa = empresa.idempresa
    # enderecoempresa = EnderecoEmpresa.query.filter_by(empresa_id=empresa.idempresa).first()
    enderecoempresa = EnderecoEmpresa.query.get(idenderecoempresa)

    if (request.method == 'POST'):
        razaoSocial = request.form.get("razaosocial")
        inscEst = request.form.get("inscricaoestadual")
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
        empresa.razaosocial = razaoSocial
        empresa.inscricaoestadual = inscEst
        empresa.cnpj = cnpj
        empresa.caixapostal = cxPostal
        empresa.email = email
        empresa.cnae_id = cnae
        empresa.telefone1 = telefone1
        empresa.telefone2 = telefone2

        # Um commit para cada tabela
        db.session.commit()

        # Atualizando no BD as informações do endereço da empresa
        enderecoempresa.cep = cep
        enderecoempresa.logradouro = logradouro
        enderecoempresa.complemento = complemento
        enderecoempresa.bairro = bairro
        enderecoempresa.estado = estado
        enderecoempresa.cidade = cidade

        db.session.commit()

        mensagem = "Empresa atualizada"
        alerta = "info"

        flash(mensagem, alerta)
        
        return redirect(url_for("listar"))
    
    return render_template("atualizar.html", empresa = empresa, cnae = cnae, endempresa = enderecoempresa)

#-------------------------------------------------------------------------------
#--------------------------- ROTAS DO FUNCIONÁRIO ------------------------------
#-------------------------------------------------------------------------------

# Rota para a página de cadastro da FUNCIONÁRIO
@app.route("/cadastrarFuncionario")
def cadastrarFuncionario():   
    empresas = Empresa.query.all()
    return render_template("cadfuncionario.html", empresas = empresas)

# Rota para carregar as informações digitadas na página de cadastro do FUNCIONÁRIO
@app.route("/cadastrofuncionario", methods=['POST'])
def cadastroFuncionario():
    if request.method == 'POST':
        empresafunc_id = request.form.get("empresa")
        nomefuncionario = request.form.get("nomefuncionario")
        nacionalidade = request.form.get("nacionalidade")
        cpf = str(request.form.get("cpf"))
        rg = str(request.form.get("identidade"))
        orgaoexpedidor = request.form.get("orgaoexpedidor")
        grauinstrucao = request.form.get("grauinstrucao")
        datanascimento = datetime.strptime(request.form.get("datanascimento"), '%d/%m/%Y')
        estadocivil = request.form.get("estadocivil")
        profissao = request.form.get("profissao")
        nomepai = request.form.get("nomepai")
        nomemae = request.form.get("nomemae")
        email = request.form.get("email")
        cargo = request.form.get("cargo")
        telefone = request.form.get("telefone")
        logradouro = request.form.get("logradouro")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        cep = str(request.form.get("cep"))

        # Aqui pode ser criada uma validação para verificar 
        # se algo foi digitado para ser gravado no BD
        funcionario = Funcionario(nomefuncionario, cpf, rg, orgaoexpedidor, grauinstrucao, nacionalidade, datanascimento, estadocivil, profissao, nomepai, nomemae, email, cargo, empresafunc_id)
        db.session.add(funcionario)

        # O comando abaixo força a criação do ID no BD
        db.session.flush()

        funcionario_id = funcionario.idfuncionario
        enderecofuncionario = EnderecoFuncionario(logradouro, complemento, bairro, cidade, estado, cep, funcionario_id = funcionario.idfuncionario)
        db.session.add(enderecofuncionario)
        db.session.commit()
        
        return redirect(url_for("index"))

# Rota para a página que exibe uma listagem dos FUNCIONÁRIOS
@app.route("/listafuncionarios")
def listaFuncionarios():
    funcionarios = Funcionario.query.all()
    empresas = Empresa.query.all()
    return render_template("listafuncionario.html", empresas = empresas, funcionarios = funcionarios)

# # Rota para exclusão de uma EMPRESA existente
# @app.route("/excluir/<int:id>")
# def excluir(id):
#     empresa = Empresa.query.get(id)
#     cnae = Cnae.query.all()

#     db.session.delete(empresa)
#     db.session.commit()

#     # Repete-se a função LISTAR pois o Flask apresenta 
#     # erro caso não seja feito dessa mameira
#     empresas = Empresa.query.all()
#     return render_template("lista.html", empresas = empresas, cnae = cnae)

# # Rota para a página de alteração do cadastro da EMPRESA
# # É importante que seja adicionado o método GET em ROUTE
# # para que traga as informações que serão alteradas
# @app.route("/atualizar/<int:id>", methods=['GET','POST'])
# def atualizar(id):
#     cnae = Cnae.query.all()
#     empresa = Empresa.query.get(id)

#     if (request.method == 'POST'):
#         razaoSocial = request.form.get("razaosocial")
#         inscEst = request.form.get("inscricaoestadual")
#         cnpj = request.form.get("cnpj")
#         cxPostal = request.form.get("caixapostal")
#         email = request.form.get("email")
#         cnae = request.form.get("cnae")
    
#         # Aqui pode ser criada uma validação para verificar 
#         # se algo foi digitado para ser gravado no BD
#         empresa.razaosocial = razaoSocial
#         empresa.inscricaoestadual = inscEst
#         empresa.cnpj = cnpj
#         empresa.caixapostal = cxPostal
#         empresa.email = email
#         empresa.cnae_id = cnae

#         db.session.commit()
        
#         return redirect(url_for("listar"))
    
#     return render_template("atualizar.html", empresa = empresa, cnae = cnae)

#-------------------------------------------------------------------------------
#---------------------------- INICIALIZAÇÃO DO APP -----------------------------
#-------------------------------------------------------------------------------
# Executa este arquivo no Flask como sendo o MAIN
# Evita-se de colocar no final da linha o comando RUN.
if __name__ == "__main__":
    app.run(host='192.168.100.190', debug=False) # Para se testar dentro da empresa
    # app.run(host='192.168.0.105', debug=True) # Para se testar dentro da empresa
    # app.run(debug=True)