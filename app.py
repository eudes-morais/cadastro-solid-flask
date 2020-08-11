import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_paginate import Pagination

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://solid:solid@172.17.0.1:5432/solid"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from classes.cnae import *
from classes.estado import Estado
from classes.empresa import Empresa
from classes.enderecoempresa import EnderecoEmpresa

# Os IMPORTS abaixo devem ficar depois do 'db = SQLAlchemy(app)', 
# para que as classes possam ser iniciadas corretamente.
#----------------------------------- IMPORTS -----------------------------------

#-------------------------------------------------------------------------------
#------------------------- Trabalhando com as rotas ----------------------------
#-------------------------------------------------------------------------------

from routes.routefuncionario import funcionario_page
app.register_blueprint(funcionario_page)

from routes.routeempresa import empresa_page
app.register_blueprint(empresa_page)

from routes.routeindex import index_page
app.register_blueprint(index_page)
# Rota para a página inicial
# from routes.routeempresa import empresa_page


# @app.route("/")
# def index():
#     return render_template("index.html")

# from routes.routefuncionario import funcionario_page
# from routes.routeempresa import empresa_page
# app.register_blueprint(funcionario_page)
# app.register_blueprint(empresa_page)

#-------------------------------------------------------------------------------
#---------------------------- INICIALIZAÇÃO DO APP -----------------------------
#-------------------------------------------------------------------------------
# Executar este arquivo no Flask como sendo MAIN, evita-se digitar RUN no prompt de comando
if __name__ == "__main__":
    # app.run(host='192.168.100.190', debug=False) # Para se testar dentro da empresa
    # app.run(host='192.168.0.105', debug=True) # Para se testar dentro da empresa
    app.run(debug=True)