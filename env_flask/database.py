import sqlite3
from werkzeug.security import generate_password_hash
import os

def get_db_connection():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('estoque.db'):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE pecas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo_oem TEXT NOT NULL UNIQUE,
            descricao TEXT,
            localizacao TEXT,
            quantidade INTEGER NOT NULL,
            preco_custo REAL NOT NULL,
            preco_venda REAL NOT NULL,
            modelo_carro TEXT NOT NULL,
            ano_carro TEXT NOT NULL
        )''')
        cur.execute('''CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )''')
        # Dados iniciais de peças
        pecas = [
            ('Filtro de Óleo', '90915-YZZF2', 'Filtro de óleo genuíno para motores Toyota.', 'A1-01', 50, 25.00, 45.00, 'Corolla', '2015-2024'),
            ('Pastilha de Freio Dianteira', '04465-YZZAA', 'Conjunto de pastilhas de freio dianteiras.', 'B2-05', 20, 120.00, 220.00, 'Hilux', '2016-2024'),
            ('Amortecedor Traseiro', '48530-02830', 'Amortecedor traseiro original.', 'C3-10', 15, 300.00, 550.00, 'Etios', '2012-2021')
        ]
        cur.executemany('''INSERT INTO pecas (nome, codigo_oem, descricao, localizacao, quantidade, preco_custo, preco_venda, modelo_carro, ano_carro) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', pecas)
        # Usuário admin padrão
        admin_hash = generate_password_hash('admin123')
        cur.execute('''INSERT INTO usuarios (username, password_hash, role) VALUES (?, ?, ?)''', ('admin', admin_hash, 'admin'))
        conn.commit()
        conn.close()
