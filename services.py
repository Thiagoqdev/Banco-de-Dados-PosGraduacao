from models import db, Cliente, Produto, Pedido, PedidoProduto
from datetime import datetime

# CRUD Cliente
def criar_cliente(nome, email, cpf, data_nascimento):
    cliente = Cliente(
        nome=nome,
        email=email,
        cpf=cpf,
        data_nascimento=datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    )
    db.session.add(cliente)
    db.session.commit()
    return cliente

def listar_clientes():
    return Cliente.query.all()

def obter_cliente(cliente_id):
    return Cliente.query.get(cliente_id)

def atualizar_cliente(cliente_id, nome=None, email=None, cpf=None, data_nascimento=None):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return None
    if nome:
        cliente.nome = nome
    if email:
        cliente.email = email
    if cpf:
        cliente.cpf = cpf
    if data_nascimento:
        cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    db.session.commit()
    return cliente

def deletar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return None
    db.session.delete(cliente)
    db.session.commit()
    return cliente

# CRUD Produto
def criar_produto(nome, preco, estoque):
    produto = Produto(nome=nome, preco=preco, estoque=estoque)
    db.session.add(produto)
    db.session.commit()
    return produto

def listar_produtos():
    return Produto.query.all()

def obter_produto(produto_id):
    return Produto.query.get(produto_id)

def atualizar_produto(produto_id, nome=None, preco=None, estoque=None):
    produto = Produto.query.get(produto_id)
    if not produto:
        return None
    if nome:
        produto.nome = nome
    if preco is not None:
        produto.preco = preco
    if estoque is not None:
        produto.estoque = estoque
    db.session.commit()
    return produto

def deletar_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return None
    db.session.delete(produto)
    db.session.commit()
    return produto

# CRUD Pedido
def criar_pedido(cliente_id, produtos_quantidades):
    pedido = Pedido(cliente_id=cliente_id, data=datetime.now())
    db.session.add(pedido)
    db.session.flush()

    for produto_id, quantidade in produtos_quantidades.items():
        item = PedidoProduto(pedido_id=pedido.id, produto_id=produto_id, quantidade=quantidade)
        db.session.add(item)
    db.session.commit()
    return pedido

def listar_pedidos():
    return Pedido.query.all()

def obter_pedido(pedido_id):
    return Pedido.query.get(pedido_id)

def deletar_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return None
    db.session.delete(pedido)
    db.session.commit()
    return pedido
