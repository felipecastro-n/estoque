# Backend - Sistema de Estoque Toyota Newland

## Requisitos
- Python 3.12+
- pip

## Instalação
1. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
2. Execute o servidor Flask:
   ```sh
   python app.py
   ```

## Endpoints principais
- Autenticação:
  - `POST /register` — Cadastro de usuário
  - `POST /login` — Login e obtenção de token JWT
- Peças:
  - `POST /pecas` — Adicionar peça (admin/estoquista)
  - `GET /pecas` — Listar peças
  - `GET /pecas/<id>` — Detalhes da peça
  - `PUT /pecas/<id>` — Atualizar peça (admin/estoquista)
  - `DELETE /pecas/<id>` — Remover peça (admin)
  - `PATCH /pecas/<id>/saida` — Registrar saída de peça
  - `PATCH /pecas/<id>/entrada` — Registrar entrada de peça
- Usuários:
  - `GET /usuarios` — Listar usuários (admin)
  - `DELETE /usuarios/<id>` — Remover usuário (admin)

## Observações
- O banco SQLite (`estoque.db`) é criado automaticamente na primeira execução, com dados de exemplo e usuário admin padrão (senha: `admin123`).
- Configure a variável `JWT_SECRET_KEY` em produção.
