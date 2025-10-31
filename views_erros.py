from leilao import app
from flask import render_template, abort


# @app.route('/area_secreta')
# def area_secreta():
#     print("Tentativa de acesso à área restritasem autenticação")
#     abort(401)


# @app.route('/painel_admin')
# def painel_admin():
#     print("Tentativa de acesso ao painel de aadmin sem permissão")
#     abort(403)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('paginaErros/404.html'), 404

@app.errorhandler(401)
def nao_autorizado(error):
    return render_template('paginaErros/401.html'), 401


@app.errorhandler(403)
def acesso_proibido(error):
    return render_template('paginaErros/403.html'), 403


