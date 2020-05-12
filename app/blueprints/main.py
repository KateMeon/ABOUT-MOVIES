from app import *
from flask import render_template, Blueprint

blueprint = Blueprint('main_api', __name__, template_folder=app.template_folder)


@blueprint.route('/')
@blueprint.route("/index")
def index_page():
    return render_template("index.html", title="ABOUT MOVIES")
