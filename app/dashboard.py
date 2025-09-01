from flask import Blueprint, jsonify
from models import db, Cliente, Produto, Venda

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/total_clientes', methods=['GET'])
def total_clientes():
    total = db.session.query(Cliente).count()
    return jsonify({'total_clientes': total})

@dashboard_bp.route('/dashboard/total_produtos', methods=['GET'])
def total_produtos():
    total = db.session.query(Produto).count()
    return jsonify({'total_produtos': total})

@dashboard_bp.route('/dashboard/total_vendas', methods=['GET'])
def total_vendas():
    total = db.session.query(Venda).count()
    return jsonify({'total_vendas': total})