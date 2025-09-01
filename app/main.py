import app
from flask import Flask, jsonify, request
from sqlalchemy.orm import joinedload
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from models import db
import sql_service
from dashboard import dashboard_bp

from nosql_service import obter_dashboard_total, registrar_dashboard_total

from models import db, Cliente, Venda, Produto

from sql_service import (
    criar_cliente, obter_cliente, listar_clientes, 
    atualizar_cliente, deletar_cliente, deletar_produto, atualizar_produto,obter_produto, obter_venda, deletar_venda
)
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

@app.route("/")
def index():
    return "Deu certo !!!"

@app.route("/clientes", methods=["GET"])
def listar_clientes_route():
    clientes = listar_clientes()
    return jsonify([
        {
            "id_cliente": c.id_cliente,
            "nome": c.nome,
            "email": c.email,
            "cpf": c.cpf,
            "data_nascimento": c.data_nascimento
        } for c in clientes
    ])

@app.route("/clientes", methods=["POST"])
def criar_cliente_route():
    data = request.json
    if not all(k in data for k in ("nome", "email")):
        return jsonify({"erro": "Campos obrigatórios: nome, email"}), 400

    cliente = criar_cliente(
        nome=data["nome"],
        email=data["email"],
        cpf=data["cpf"],
        data_nascimento=data["data_nascimento"]
    )

    total_clientes = len(listar_clientes())
    registrar_dashboard_total(total_clientes)

    return jsonify({"id": cliente.id_cliente, "mensagem": "Cliente criado com sucesso"}), 201

@app.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def deletar_cliente_route(cliente_id):
    cliente = deletar_cliente(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    total_clientes = len(listar_clientes())
    registrar_dashboard_total(total_clientes)

    return jsonify({"mensagem": "Cliente deletado com sucesso"})

@app.route("/clientes/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente_route(cliente_id):
    data = request.json
    cliente = atualizar_cliente(
        cliente_id,
        nome=data.get("nome"),
        email=data.get("email"),
        cpf=data.get("cpf"),
        data_nascimento=data.get("data_nascimento")
    )
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({"mensagem": "Cliente atualizado com sucesso"})

@app.route("/clientes/<int:cliente_id>", methods=["GET"])
def obter_cliente_route(cliente_id):
    cliente = obter_cliente(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({
        "id": cliente.id_cliente,
        "nome": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "data_nascimento": cliente.data_nascimento.strftime("%d-%m-%Y")
    })

# Produtos

@app.route("/produtos", methods=["GET"])
def get_produtos():
    produtos = sql_service.listar_produtos()
    return jsonify([{"id": p.id_produto, "nome": p.nome, "preco": p.preco, "descricao": p.descricao, "categoria": p.categoria} for p in produtos])

"""@app.route("/produtos", methods=["POST"])
def post_produto():
    data = request.json
    produto = sql_service.criar_produto(data["nome"], data["preco"], data["descricao"], data["categoria"])
    return jsonify({"id": produto.id_produto}), 201
"""

@app.route("/produtos", methods=["POST"])
def post_produto():
    data = request.json
    produto = sql_service.criar_produto(data["nome"], data["preco"], data["descricao"], data["categoria"])

    from nosql_service import registrar_dashboard_total_produtos

    total_produtos = len(sql_service.listar_produtos())
    registrar_dashboard_total_produtos(total_produtos)

    return jsonify({"id": produto.id_produto}), 201

@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto_route(produto_id):
    produto = deletar_produto(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    from nosql_service import registrar_dashboard_total_produtos
    total_produtos = len(sql_service.listar_produtos())
    registrar_dashboard_total_produtos(total_produtos)

    return jsonify({"mensagem": "Produto deletado com sucesso"})

@app.route("/produtos/<int:id_produto>", methods=["PUT"])
def atualizar_produto_route(id_produto):
    data = request.json
    produto = atualizar_produto(
        id_produto,
        nome=data.get("nome"),
        preco=data.get("preco"),
        estoque=data.get("estoque")
    )
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"mensagem": "Produto atualizado com sucesso!"})

@app.route("/produtos/<int:id_produto>", methods=["GET"])
def obter_produto_route(id_produto):
    produto = obter_produto(id_produto)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({
        "id": produto.id_produto,
        "nome": produto.nome,
        "preco": produto.preco,
        "descricao": produto.descricao,
        "categoria": produto.categoria
    })

# Vendas

@app.route("/vendas", methods=["GET"])
def listar_vendas_route():
    pedidos = Venda.query.options(
        joinedload(Venda.cliente),
        joinedload(Venda.produto)
    ).all()

    result = []
    for v in pedidos:
        result.append({
            "id": v.id_pedido,
            "data_pedido": v.data_pedido,
            "cliente": v.cliente.nome if v.cliente else None,
            "produto": v.produto.nome if v.produto else None,
            "valor_total": v.valor_total
        })

    return jsonify(result)

@app.route("/vendas", methods=["POST"])
def post_venda():
    data = request.json
    venda = sql_service.criar_venda(data["id_cliente"], data["id_produto"], data["valor_total"])
    if not venda:
        return jsonify({"erro": "Produto inexistente ou estoque insuficiente"}), 400
    from nosql_service import registrar_dashboard_total_vendas
    total_vendas = len(sql_service.listar_vendas())
    registrar_dashboard_total_vendas(total_vendas)

    return jsonify({"id": venda.id_pedido}), 201

@app.route("/vendas/<int:id_pedido>", methods=["PUT"])
def atualizar_vendas_route(id_pedido):
    data = request.json
    venda = sql_service.atualizar_venda(data["id_cliente"], data["id_produdo"], data["valor_total"])
    if not venda:
        return jsonify({"erro": "Pedido não encontrado, entre em contato com o administrador"}), 404
    return jsonify({"id": venda.id_pedido}), 201

@app.route("/vendas/<int:id_pedido>", methods=["GET"])
def obter_vendas_route(id_pedido):
    venda = obter_venda(id_pedido)
    if not venda:
        return jsonify({"erro": "Venda não encontrada"}), 404
    
    return jsonify({
        "id_pedido": venda.id_pedido,
        "id_cliente": venda.id_cliente,
        "id_produto": venda.id_produto,
        "data_pedido": venda.data_pedido.strftime("%d-%m-%Y %H:%M:%S"),
        "valor_total": venda.valor_total
    })

@app.route("/vendas/<int:id_pedido>", methods=["DELETE"])
def deletar_vendas_route(id_pedido):
    venda = deletar_venda(id_pedido) # Chama a função do sql_service
    if not venda:
        return jsonify({"erro": "Venda não encontrada"}), 404

    from nosql_service import registrar_dashboard_total_vendas
    total_vendas = len(sql_service.listar_vendas())
    registrar_dashboard_total_vendas(total_vendas)

    return jsonify({"mensagem": "Venda deletada com sucesso"})

app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# MongoDB - Relatórios

@app.route("/dashboard/total_clientes", methods=["GET"])
def dashboard_total_clientes():
    total = obter_dashboard_total()
    return jsonify({"total_clientes": total})

@app.route("/dashboard/total_produtos", methods=["GET"])
def dashboard_total_produtos():
    from nosql_service import obter_dashboard_total_produtos
    total = obter_dashboard_total_produtos()
    return jsonify({"total_produtos": total})

@app.route("/dashboard/total_vendas", methods=["GET"])
def dashboard_total_vendas():
    from nosql_service import obter_dashboard_total_vendas
    total = obter_dashboard_total_vendas()
    return jsonify({"total_vendas": total})

