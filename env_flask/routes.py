from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db_connection
import sqlite3

bp = Blueprint('api', __name__)

# --- Autenticação ---
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'estoquista')
    if not username or not password:
        return jsonify({'error': 'Usuário e senha são obrigatórios.'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO usuarios (username, password_hash, role) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), role))
        conn.commit()
        return jsonify({'message': 'Usuário registrado com sucesso.'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Usuário já existe.'}), 409
    finally:
        conn.close()

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Usuário e senha são obrigatórios.'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    user = cur.fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity={'id': user['id'], 'username': user['username'], 'role': user['role']})
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Credenciais inválidas.'}), 401

# --- Decoradores de permissão ---
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            return jsonify({'error': 'Acesso restrito ao administrador.'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def estoquista_or_admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity['role'] not in ['admin', 'estoquista']:
            return jsonify({'error': 'Acesso restrito.'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

# --- Rotas de Peças ---
@bp.route('/pecas', methods=['POST'])
@estoquista_or_admin_required
def add_peca():
    data = request.get_json()
    required = ['nome', 'codigo_oem', 'descricao', 'localizacao', 'quantidade', 'preco_custo', 'preco_venda', 'modelo_carro', 'ano_carro']
    if not all(field in data for field in required):
        return jsonify({'error': 'Campos obrigatórios faltando.'}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO pecas (nome, codigo_oem, descricao, localizacao, quantidade, preco_custo, preco_venda, modelo_carro, ano_carro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (data['nome'], data['codigo_oem'], data['descricao'], data['localizacao'], data['quantidade'], data['preco_custo'], data['preco_venda'], data['modelo_carro'], data['ano_carro']))
        conn.commit()
        return jsonify({'message': 'Peça adicionada com sucesso.'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Código OEM já cadastrado.'}), 409
    finally:
        conn.close()

@bp.route('/pecas', methods=['GET'])
@jwt_required()
def list_pecas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pecas')
    pecas = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(pecas), 200

@bp.route('/pecas/<int:peca_id>', methods=['GET'])
@jwt_required()
def get_peca(peca_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,))
    peca = cur.fetchone()
    conn.close()
    if not peca:
        return jsonify({'error': 'Peça não encontrada.'}), 404
    return jsonify(dict(peca)), 200

@bp.route('/pecas/<int:peca_id>', methods=['PUT'])
@estoquista_or_admin_required
def update_peca(peca_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'error': 'Peça não encontrada.'}), 404
    fields = ['nome', 'codigo_oem', 'descricao', 'localizacao', 'quantidade', 'preco_custo', 'preco_venda', 'modelo_carro', 'ano_carro']
    updates = ', '.join([f"{f} = ?" for f in fields if f in data])
    values = [data[f] for f in fields if f in data]
    if not updates:
        conn.close()
        return jsonify({'error': 'Nenhum campo para atualizar.'}), 400
    try:
        cur.execute(f'UPDATE pecas SET {updates} WHERE id = ?', (*values, peca_id))
        conn.commit()
        return jsonify({'message': 'Peça atualizada com sucesso.'}), 200
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Código OEM já cadastrado.'}), 409
    finally:
        conn.close()

@bp.route('/pecas/<int:peca_id>', methods=['DELETE'])
@admin_required
def delete_peca(peca_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'error': 'Peça não encontrada.'}), 404
    cur.execute('DELETE FROM pecas WHERE id = ?', (peca_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Peça removida com sucesso.'}), 200

@bp.route('/pecas/<int:peca_id>/saida', methods=['PATCH'])
@estoquista_or_admin_required
def saida_peca(peca_id):
    data = request.get_json()
    quantidade = data.get('quantidade')
    if not isinstance(quantidade, int) or quantidade <= 0:
        return jsonify({'error': 'Quantidade inválida.'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT quantidade FROM pecas WHERE id = ?', (peca_id,))
    peca = cur.fetchone()
    if not peca:
        conn.close()
        return jsonify({'error': 'Peça não encontrada.'}), 404
    if peca['quantidade'] < quantidade:
        conn.close()
        return jsonify({'error': 'Estoque insuficiente.'}), 400
    cur.execute('UPDATE pecas SET quantidade = quantidade - ? WHERE id = ?', (quantidade, peca_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Saída registrada com sucesso.'}), 200

@bp.route('/pecas/<int:peca_id>/entrada', methods=['PATCH'])
@estoquista_or_admin_required
def entrada_peca(peca_id):
    data = request.get_json()
    quantidade = data.get('quantidade')
    if not isinstance(quantidade, int) or quantidade <= 0:
        return jsonify({'error': 'Quantidade inválida.'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT quantidade FROM pecas WHERE id = ?', (peca_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'error': 'Peça não encontrada.'}), 404
    cur.execute('UPDATE pecas SET quantidade = quantidade + ? WHERE id = ?', (quantidade, peca_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Entrada registrada com sucesso.'}), 200

# --- Rotas de Usuário ---
@bp.route('/usuarios', methods=['GET'])
@admin_required
def list_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, role FROM usuarios')
    usuarios = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(usuarios), 200

@bp.route('/usuarios/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_usuario(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'error': 'Usuário não encontrado.'}), 404
    cur.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Usuário removido com sucesso.'}), 200

@bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'API Estoque Toyota Newland'}), 200
