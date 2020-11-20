import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_paginate import Pagination

app = Flask(__name__)
app.secret_key = os.urandom(24)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://solid:solid@172.17.0.2:5432/solid"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://solid:solid@192.168.0.105:5432/solid"

# Na configuração do SQLALCHEMY_DATABASE_URI teve que ser adicionada (após o schema do banco)
# as variáveis SSLMODE, SSLROOTCERT, SSLCERT e SSLKEY
# Também foi direcionado para fora do HD onde estava armazenado, pois ele não deixava
# mudar as permissões do arquivo SSLKEY
sqlalchemyuri = "postgresql://solid:solid@35.247.252.238:5432/solid?"
sqlalchemyuri = sqlalchemyuri + "sslmode=verify-ca&"
sqlalchemyuri = sqlalchemyuri + "sslrootcert=/home/eudes/certificados/server-ca.pem&"
sqlalchemyuri = sqlalchemyuri + "sslcert=/home/eudes/certificados/client-cert.pem&"
sqlalchemyuri = sqlalchemyuri + "sslkey=/home/eudes/certificados/client-key.pem"
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemyuri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from classes.cnae import *
from classes.estado import Estado
from classes.empresa import Empresa
from classes.enderecoempresa import EnderecoEmpresa
from classes.orgao import Orgao
from classes.licenca import Licenca

# Os IMPORTS abaixo devem ficar depois do 'db = SQLAlchemy(app)', 
# para que as classes possam ser iniciadas corretamente.
#----------------------------------- IMPORTS -----------------------------------

#-------------------------------------------------------------------------------
#------------------------- Trabalhando com as rotas ----------------------------
#-------------------------------------------------------------------------------
from routes.routelap import lap_page
app.register_blueprint(lap_page)

from routes.routelicenca import licenca_page
app.register_blueprint(licenca_page)

from routes.routeorgao import orgao_page
app.register_blueprint(orgao_page)

from routes.routefuncionario import funcionario_page
app.register_blueprint(funcionario_page)

from routes.routeempresa import empresa_page
app.register_blueprint(empresa_page)

from routes.routeindex import index_page
app.register_blueprint(index_page)

# @app.route("/")
# def index():
#     return render_template("index.html")

#-------------------------------------------------------------------------------
#---------------------------- INICIALIZAÇÃO DO APP -----------------------------
#-------------------------------------------------------------------------------
# Executar este arquivo no Flask como sendo MAIN, evita-se digitar RUN no prompt de comando
if __name__ == "__main__":
    # app.run(host='192.168.100.190', debug=False) # Para se testar dentro da empresa
    # app.run(host='192.168.0.102', debug=True) # Para se testar dentro da empresa
    # app.run(host='192.168.100.6', debug=False)
    app.run(debug=True)