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
            ano_carro TEXT NOT NULL,
            rfid_uid TEXT UNIQUE
        )''')
        cur.execute('''CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )''')
        # Registros reais de peças automotivas, sem duplicações
        pecas_reais = [
            ('Filtro de Óleo', '90915-YZZF2', 'Filtro de óleo genuíno para motores Toyota.', 'A1-01', 50, 25.00, 45.00, 'Corolla', '2015-2024'),
            ('Pastilha de Freio Dianteira', '04465-YZZAA', 'Conjunto de pastilhas de freio dianteiras.', 'B2-05', 20, 120.00, 220.00, 'Hilux', '2016-2024'),
            ('Amortecedor Traseiro', '48530-02830', 'Amortecedor traseiro original.', 'C3-10', 15, 300.00, 550.00, 'Etios', '2012-2021'),
            ('Filtro de Ar', '17801-0D020', 'Filtro de ar genuíno para motores Toyota.', 'A1-02', 40, 30.00, 55.00, 'Corolla', '2015-2024'),
            ('Vela de Ignição', '90919-01253', 'Vela de ignição original Toyota.', 'A2-01', 60, 18.00, 35.00, 'Corolla', '2015-2024'),
            ('Disco de Freio Dianteiro', '43512-0D120', 'Disco de freio dianteiro ventilado.', 'B2-06', 25, 180.00, 320.00, 'Hilux', '2016-2024'),
            ('Bomba de Combustível', '23220-0C050', 'Bomba de combustível elétrica.', 'C1-01', 10, 400.00, 700.00, 'Etios', '2012-2021'),
            ('Sensor de Oxigênio', '89465-0D170', 'Sensor de oxigênio original.', 'C2-01', 18, 150.00, 270.00, 'Corolla', '2015-2024'),
            ('Correia Dentada', '13568-09070', 'Correia dentada reforçada.', 'D1-01', 30, 90.00, 160.00, 'Hilux', '2016-2024'),
            ('Radiador', '16400-0D240', 'Radiador de alumínio.', 'D2-01', 8, 600.00, 950.00, 'Corolla', '2015-2024'),
            ('Coxim do Motor', '12361-0D120', 'Coxim de motor dianteiro.', 'E1-01', 22, 80.00, 150.00, 'Etios', '2012-2021'),
            ('Bieleta', '48820-0D020', 'Bieleta da barra estabilizadora.', 'E2-01', 35, 25.00, 50.00, 'Corolla', '2015-2024'),
            ('Rolamento de Roda', '90369-54006', 'Rolamento de roda traseira.', 'F1-01', 16, 110.00, 200.00, 'Hilux', '2016-2024'),
            ('Kit Embreagem', '31250-0K020', 'Kit de embreagem completo.', 'F2-01', 12, 350.00, 600.00, 'Etios', '2012-2021'),
            ('Amortecedor Dianteiro', '48510-09B60', 'Amortecedor dianteiro original.', 'G1-01', 14, 320.00, 580.00, 'Corolla', '2015-2024'),
            ('Bomba d’Água', '16100-39436', 'Bomba d’água para sistema de arrefecimento.', 'G2-01', 9, 210.00, 370.00, 'Hilux', '2016-2024'),
            ('Sensor de Fase', '90919-05049', 'Sensor de fase do comando.', 'H1-01', 20, 60.00, 110.00, 'Etios', '2012-2021'),
            ('Cilindro Mestre', '47201-0D120', 'Cilindro mestre de freio.', 'H2-01', 7, 250.00, 420.00, 'Corolla', '2015-2024'),
            ('Cabo de Vela', '90919-21564', 'Cabo de vela de ignição.', 'I1-01', 28, 35.00, 65.00, 'Hilux', '2016-2024'),
            ('Filtro de Combustível', '23300-0D020', 'Filtro de combustível original.', 'I2-01', 45, 22.00, 40.00, 'Etios', '2012-2021'),
            ('Junta do Cabeçote', '11115-0D020', 'Junta do cabeçote reforçada.', 'J1-01', 11, 95.00, 170.00, 'Corolla', '2015-2024'),
            ('Sensor ABS', '89543-0D120', 'Sensor ABS dianteiro.', 'J2-01', 13, 130.00, 240.00, 'Hilux', '2016-2024'),
            ('Coxim do Amortecedor', '48609-0D120', 'Coxim superior do amortecedor.', 'K1-01', 17, 40.00, 75.00, 'Etios', '2012-2021'),
            ('Sensor de Pressão', '89458-60010', 'Sensor de pressão do óleo.', 'L1-01', 10, 80.00, 150.00, 'Corolla', '2015-2024'),
            ('Bomba de Óleo', '15100-0D010', 'Bomba de óleo original.', 'L2-01', 12, 250.00, 400.00, 'Hilux', '2016-2024'),
            ('Interruptor de Freio', '84340-69025', 'Interruptor do pedal de freio.', 'M1-01', 15, 35.00, 65.00, 'Etios', '2012-2021'),
            ('Mangueira de Radiador', '16572-0D020', 'Mangueira superior do radiador.', 'M2-01', 20, 25.00, 45.00, 'Corolla', '2015-2024'),
            ('Termostato', '90916-03093', 'Termostato do sistema de arrefecimento.', 'N1-01', 18, 60.00, 110.00, 'Hilux', '2016-2024'),
            ('Sensor de Temperatura', '89422-33030', 'Sensor de temperatura do motor.', 'N2-01', 14, 45.00, 80.00, 'Etios', '2012-2021'),
            ('Cabo de Bateria', '90982-05035', 'Cabo positivo da bateria.', 'O1-01', 16, 30.00, 55.00, 'Corolla', '2015-2024'),
            ('Motor de Partida', '28100-0D040', 'Motor de partida original.', 'O2-01', 8, 400.00, 700.00, 'Hilux', '2016-2024'),
            ('Alternador', '27060-0D040', 'Alternador genuíno.', 'P1-01', 9, 600.00, 950.00, 'Etios', '2012-2021'),
            ('Sensor de Velocidade', '89543-0D130', 'Sensor de velocidade da roda.', 'P2-01', 11, 130.00, 240.00, 'Corolla', '2015-2024'),
            ('Coxim de Suspensão', '48609-0D130', 'Coxim inferior da suspensão.', 'Q1-01', 13, 40.00, 75.00, 'Hilux', '2016-2024'),
            ('Bieleta Traseira', '48820-0D030', 'Bieleta traseira.', 'Q2-01', 17, 25.00, 50.00, 'Etios', '2012-2021'),
            ('Rolamento Dianteiro', '90369-54007', 'Rolamento de roda dianteira.', 'R1-01', 19, 110.00, 200.00, 'Corolla', '2015-2024'),
            ('Kit de Embreagem', '31250-0K030', 'Kit de embreagem reforçado.', 'R2-01', 21, 350.00, 600.00, 'Hilux', '2016-2024'),
            ('Amortecedor Esportivo', '48510-09B70', 'Amortecedor dianteiro esportivo.', 'S1-01', 14, 320.00, 580.00, 'Etios', '2012-2021'),
            ('Bomba de Água Elétrica', '16100-39437', 'Bomba d’água elétrica.', 'S2-01', 9, 210.00, 370.00, 'Corolla', '2015-2024'),
            ('Sensor de Posição', '90919-05050', 'Sensor de posição do comando.', 'T1-01', 20, 60.00, 110.00, 'Hilux', '2016-2024'),
            ('Cilindro Auxiliar', '47201-0D130', 'Cilindro auxiliar de freio.', 'T2-01', 7, 250.00, 420.00, 'Etios', '2012-2021'),
            ('Cabo de Embreagem', '90919-21565', 'Cabo de embreagem.', 'U1-01', 28, 35.00, 65.00, 'Corolla', '2015-2024'),
            ('Filtro de Ar Esportivo', '17801-0D030', 'Filtro de ar esportivo.', 'U2-01', 45, 22.00, 40.00, 'Hilux', '2016-2024'),
            ('Junta de Cabeçote Reforçada', '11115-0D030', 'Junta de cabeçote reforçada.', 'V1-01', 11, 95.00, 170.00, 'Etios', '2012-2021'),
            ('Sensor ABS Traseiro', '89543-0D130', 'Sensor ABS traseiro.', 'V2-01', 13, 130.00, 240.00, 'Corolla', '2015-2024'),
            ('Coxim do Motor Traseiro', '12361-0D130', 'Coxim de motor traseiro.', 'W1-01', 22, 80.00, 150.00, 'Hilux', '2016-2024'),
            ('Bieleta Esportiva', '48820-0D030', 'Bieleta esportiva.', 'W2-01', 35, 25.00, 50.00, 'Etios', '2012-2021'),
            ('Rolamento de Roda Esportivo', '90369-54008', 'Rolamento esportivo.', 'X1-01', 16, 110.00, 200.00, 'Corolla', '2015-2024'),
            ('Kit Embreagem Esportivo', '31250-0K040', 'Kit de embreagem esportivo.', 'X2-01', 12, 350.00, 600.00, 'Hilux', '2016-2024'),
            ('Amortecedor Traseiro Esportivo', '48530-02840', 'Amortecedor traseiro esportivo.', 'Y1-01', 15, 300.00, 550.00, 'Etios', '2012-2021'),
            ('Filtro de Combustível Esportivo', '23300-0D030', 'Filtro de combustível esportivo.', 'Y2-01', 45, 22.00, 40.00, 'Corolla', '2015-2024'),
            ('Sensor de Oxigênio Esportivo', '89465-0D180', 'Sensor de oxigênio esportivo.', 'Z1-01', 18, 150.00, 270.00, 'Hilux', '2016-2024'),
            ('Correia Dentada Esportiva', '13568-09080', 'Correia dentada esportiva.', 'Z2-01', 30, 90.00, 160.00, 'Etios', '2012-2021'),
        ]
        # Insere apenas registros com codigo_oem único
        pecas_unicas = []
        codigos_vistos = set()
        for p in pecas_reais:
            if p[1] not in codigos_vistos:
                pecas_unicas.append(p)
                codigos_vistos.add(p[1])
        cur.executemany('''INSERT INTO pecas (nome, codigo_oem, descricao, localizacao, quantidade, preco_custo, preco_venda, modelo_carro, ano_carro) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', pecas_unicas)
        # Usuário admin padrão
        admin_hash = generate_password_hash('admin123')
        cur.execute('''INSERT INTO usuarios (username, password_hash, role) VALUES (?, ?, ?)''', ('admin', admin_hash, 'admin'))
        conn.commit()
        conn.close()
