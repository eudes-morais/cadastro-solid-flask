import psycopg2
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://solid:solid@172.17.0.1:5432/solid"
db = SQLAlchemy(app)


#-------------------------------------- Classe Empresa -----------------------------------------------
class Empresa(db.Model):
    __tablename__ = 'empresa'
    idempresa = db.Column(db.Integer, primary_key=True)
    razaosocial = db.Column(db.String(150))
    inscricaoestadual = db.Column(db.String(15))
    cnpj = db.Column(db.String(14))
    caixapostal = db.Column(db.String(10))
    email = db.Column(db.String(50))
    cnae_id = db.Column(db.Integer)

    # Método construtor
    def __init__(self, razaosocial, inscricaoestadual, cnpj, caixapostal, email, cnae_id):
        self.razaosocial = razaosocial
        self.inscricaoestadual = inscricaoestadual
        self.cnpj = cnpj
        self.caixapostal = caixapostal
        self.email = email
        self.cnae_id = cnae_id

# Caso seja necessário criar o BD
#db.create_all()

#-------------------------------------- Classe CNAE -----------------------------------------------
class Cnae(db.Model):
    __tablename__ = 'cnae'
    idcnae = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(7))
    descricao = db.Column(db.String(200))
    
    # Método construtor
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

#-------------------------------------- Classe Endereço -----------------------------------------------
class Endereco(db.Model):
    __tablename__ = 'endereco'
    idendereco = db.Column(db.Integer, primary_key=True)
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

#-------------------------------------- Classe Telefone -------------------------------------------
class Telefone(db.Model):
    __tablename__ = 'telefone'
    idtelefone = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.Integer)
    numero = db.Column(db.Integer)
    empresa = db.Column(db.Integer)
    funcionario = db.Column(db.Integer)
    orgao = db.Column(db.Integer)
    
    # Método construtor
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

# Trabalhando com as rotas
# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

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
        print(empresa.idempresa)

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
    # erro caso não seja feito conforme está abaixo
    empresas = Empresa.query.all()
    return render_template("lista.html", empresas = empresas, cnae = cnae)

# Rota para a página de alteração do cadastro. É importante que seja adicionado o
# método GET em ROUTE para que possa ser trazido as informações que serão alteradas
@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    cnae = Cnae.query.all()
    empresa = Empresa.query.get(id)

    if request.method == 'POST':
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
        empresa.cnae = cnae

        db.session.commit()
        
        return redirect(url_for("listar"))
    
    return render_template("atualizar.html", empresa = empresa, cnae = cnae)

# Executa este arquivo no Flask como sendo o MAIN
# Evita-se de colocar no final da linha o comando RUN.
if __name__ == "__main__":
    app.run(debug=True)