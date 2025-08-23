from flask import Flask, request, jsonify
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, Cliente, Produto, Pedido, PedidoProduto
import services
from nosql_service import obter_dashborad_total

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "API CRUD Clientes, Produtos e Pedidos"

# Rotas Cliente
@app.route('/clientes', methods=['GET'])
def listar_clientes_route():
    clientes = services.listar_clientes()
    return jsonify([{
        "id": c.id,
        "nome": c.nome,
        "email": c.email,
        "cpf": c.cpf,
        "data_nascimento": c.data_nascimento.strftime("%Y-%m-%d")
    } for c in clientes])

@app.route('/clientes', methods=['POST'])
def criar_cliente_route():
    data = request.json
    cliente = services.criar_cliente(
        data['nome'], data['email'], data['cpf'], data['data_nascimento']
    )
    return jsonify({"id": cliente.id}), 201

@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def obter_cliente_route(cliente_id):
    cliente = services.obter_cliente(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "data_nascimento": cliente.data_nascimento.strftime("%Y-%m-%d")
    })

@app.route('/clientes/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente_route(cliente_id):
    data = request.json
    cliente = services.atualizar_cliente(
        cliente_id,
        nome=data.get('nome'),
        email=data.get('email'),
        cpf=data.get('cpf'),
        data_nascimento=data.get('data_nascimento')
    )
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({"msg": "Cliente atualizado"})

@app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def deletar_cliente_route(cliente_id):
    cliente = services.deletar_cliente(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({"msg": "Cliente deletado"})

# Rotas Produto
@app.route('/produtos', methods=['GET'])
def listar_produtos_route():
    produtos = services.listar_produtos()
    return jsonify([{
        "id": p.id,
        "nome": p.nome,
        "preco": p.preco,
        "estoque": p.estoque
    } for p in produtos])

@app.route('/produtos', methods=['POST'])
def criar_produto_route():
    data = request.json
    produto = services.criar_produto(
        data['nome'], data['preco'], data['estoque']
    )
    return jsonify({"id": produto.id}), 201

@app.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto_route(produto_id):
    produto = services.obter_produto(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({
        "id": produto.id,
        "nome": produto.nome,
        "preco": produto.preco,
        "estoque": produto.estoque
    })

@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto_route(produto_id):
    data = request.json
    produto = services.atualizar_produto(
        produto_id,
        nome=data.get('nome'),
        preco=data.get('preco'),
        estoque=data.get('estoque')
    )
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"msg": "Produto atualizado"})

@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto_route(produto_id):
    produto = services.deletar_produto(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"msg": "Produto deletado"})

# Rotas Pedido
@app.route('/pedidos', methods=['GET'])
def listar_pedidos_route():
    pedidos = services.listar_pedidos()
    return jsonify([{
        "id": p.id,
        "cliente_id": p.cliente_id,
        "data": p.data.strftime("%Y-%m-%d %H:%M:%S"),
        "produtos": [
            {"produto_id": item.produto_id, "quantidade": item.quantidade}
            for item in p.produtos
        ]
    } for p in pedidos])

@app.route('/pedidos', methods=['POST'])
def criar_pedido_route():
    data = request.json
    pedido = services.criar_pedido(
        data['cliente_id'],
        data['produtos']  # Exemplo: {"1": 2, "3": 1} (produto_id: quantidade)
    )
    return jsonify({"id": pedido.id}), 201

@app.route('/pedidos/<int:pedido_id>', methods=['GET'])
def obter_pedido_route(pedido_id):
    pedido = services.obter_pedido(pedido_id)
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404
    return jsonify({
        "id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "data": pedido.data.strftime("%Y-%m-%d %H:%M:%S"),
        "produtos": [
            {"produto_id": item.produto_id, "quantidade": item.quantidade}
            for item in pedido.produtos
        ]
    })

@app.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def deletar_pedido_route(pedido_id):
    pedido = services.deletar_pedido(pedido_id)
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404
    return jsonify({"msg": "Pedido deletado"})


@app.route('/produtos/<int:produto_id>', methods=['GET'])
def dashboard_total_clientes():
    total = obter_dashborad_total()
    return jsonify({"Total clientes"}, total)

if __name__ == '__main__':
    app.run(debug=True)

