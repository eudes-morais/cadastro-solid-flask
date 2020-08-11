from flask import Blueprint, render_template
# Rota para a página inicial
index_page = Blueprint('index_page', __name__, template_folder='routes')
@index_page.route("/")
def index():
    return render_template("index.html")