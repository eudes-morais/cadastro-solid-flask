import psycopg2
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://solid:solid@172.17.0.1:5432/solid"
db = SQLAlchemy(app)

# Os IMPORTS abaixo devem ficar depois do 'db = SQLAlchemy(app)', para que eles possam ser iniciados na classe
from classes.cnae import *
from classes.empresa import *
from classes.endereco import *
    


# Trabalhando com as rotas
# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

#----------------------- Funções referentes à EMPRESA --------------------------

# Rota para a página de cadastro 
@app.route("/cadastrar")
def cadastrar():
    
    cnae = Cnae.query.all()
    return render_template("cadastro.html", cnae = cnae)

# Rota para carregar as informações digitadas na página de cadastro (cadastro.html)
@app.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == 'POST':
        razaoSocial = request.form.get("razaosocial")
        inscEst = request.form.get("inscricaoestadual")
        cnpj = request.form.get("cnpj")
        cxPostal = request.form.get("caixapostal")
        email = request.form.get("email")
        cnae_id = str(request.form.get("cnae"))
        telefone = str(request.form.get("telefone"))
        logradouro = request.form.get("logradouro")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        cep = str(request.form.get("cep"))

        # Aqui pode ser criada uma validação para verificar 
        # se algo foi digitado para ser gravado no BD
        empresa = Empresa(razaoSocial, inscEst, cnpj, cxPostal, email, cnae_id)
        db.session.add(empresa)

        # O comando abaixo força a criação do ID no BD
        db.session.flush()

        empresa_id = empresa.idempresa
        endereco = Endereco(logradouro, complemento, bairro, cidade, estado, cep, empresa_id=empresa.idempresa)
        db.session.add(endereco)
        db.session.commit()
        
        return redirect(url_for("index"))

# Rota para a página que exibe uma listagem das empresas
@app.route("/lista")
def listar():
    empresas = Empresa.query.all()
    print(len(empresas))

    cnae = Cnae.query.all()
    return render_template("lista.html", empresas = empresas, cnae = cnae)

@app.route("/excluir/<int:id>")
def excluir(id):
    empresa = Empresa.query.get(id)
    cnae = Cnae.query.all()
    # empresa = Empresa.query.filter_by(id=id).first()

    db.session.delete(empresa)
    db.session.commit()

    # Repete-se a função LISTAR pois o Flask apresenta 
    # erro caso não seja feito dessa mameira
    empresas = Empresa.query.all()
    return render_template("lista.html", empresas = empresas, cnae = cnae)

# Rota para a página de alteração do cadastro. É importante que seja adicionado o
# método GET em ROUTE para que possa ser trazido as informações que serão alteradas
@app.route("/atualizar/<int:id>", methods=['GET','POST'])
def atualizar(id):
    cnae = Cnae.query.all()
    empresa = Empresa.query.get(id)

    if (request.method == 'POST'):
        razaoSocial = request.form.get("razaosocial")
        inscEst = request.form.get("inscricaoestadual")
        cnpj = request.form.get("cnpj")
        cxPostal = request.form.get("caixapostal")
        email = request.form.get("email")
        cnae = request.form.get("cnae")
    
        # Aqui pode ser criada uma validação para verificar 
        # se algo foi digitado para ser gravado no BD
        empresa.razaosocial = razaoSocial
        empresa.inscricaoestadual = inscEst
        empresa.cnpj = cnpj
        empresa.caixapostal = cxPostal
        empresa.email = email
        empresa.cnae_id = cnae

        db.session.commit()
        
        return redirect(url_for("listar"))
    
    return render_template("atualizar.html", empresa = empresa, cnae = cnae)

#----------------------- Funções referentes ao FUNCIONÁRIO --------------------------

@app.route("/cadastrarFunc")
def cadastrarFunc():
    empresas = Empresas.query.all()
    return render_template("cadastrofuncionario.html", empresas = empresas)

# Executa este arquivo no Flask como sendo o MAIN
# Evita-se de colocar no final da linha o comando RUN.
if __name__ == "__main__":
    # app.run(host='192.168.100.190', debug=False)
    app.run(debug=True)