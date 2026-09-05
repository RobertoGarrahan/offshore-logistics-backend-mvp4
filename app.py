from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offshore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==========================================
# MODELO DO BANCO DE DADOS
# ==========================================
class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    servico = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "cep": self.cep,
            "cidade": self.cidade,
            "servico": self.servico
        }

# Cria o banco de dados e as tabelas na primeira execução
with app.app_context():
    db.create_all()

# ==========================================
# ROTAS CRUD (GET, POST, PUT, DELETE)
# ==========================================

# 1. POST: Cadastrar um novo fornecedor
@app.route('/fornecedores', methods=['POST'])
def add_fornecedor():
    data = request.get_json()
    novo_fornecedor = Fornecedor(
        nome=data['nome'],
        cnpj=data['cnpj'],
        cep=data['cep'],
        cidade=data['cidade'],
        servico=data['servico']
    )
    db.session.add(novo_fornecedor)
    db.session.commit()
    return jsonify({"message": "Fornecedor cadastrado com sucesso!", "fornecedor": novo_fornecedor.to_dict()}), 201

# 2. GET: Listar todos os fornecedores
@app.route('/fornecedores', methods=['GET'])
def get_fornecedores():
    fornecedores = Fornecedor.query.all()
    return jsonify([f.to_dict() for f in fornecedores]), 200

# 3. PUT: Atualizar um fornecedor existente
@app.route('/fornecedores/<int:id>', methods=['PUT'])
def update_fornecedor(id):
    data = request.get_json()
    fornecedor = Fornecedor.query.get_or_404(id)
    
    fornecedor.nome = data.get('nome', fornecedor.nome)
    fornecedor.cnpj = data.get('cnpj', fornecedor.cnpj)
    fornecedor.cep = data.get('cep', fornecedor.cep)
    fornecedor.cidade = data.get('cidade', fornecedor.cidade)
    fornecedor.servico = data.get('servico', fornecedor.servico)
    
    db.session.commit()
    return jsonify({"message": "Fornecedor atualizado com sucesso!", "fornecedor": fornecedor.to_dict()}), 200

# 4. DELETE: Remover um fornecedor
@app.route('/fornecedores/<int:id>', methods=['DELETE'])
def delete_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return jsonify({"message": "Fornecedor removido com sucesso!"}), 200

# ==========================================
# ROTA DE INTEGRAÇÃO COM API EXTERNA
# ==========================================

# 5. GET: Buscar clima de um porto via Open-Meteo
@app.route('/porto/clima', methods=['GET'])
def get_clima_porto():
    # Parâmetros padrão apontando para o Porto de Macaé caso não sejam enviados
    lat = request.args.get('lat', '-22.3708')
    lon = request.args.get('lon', '-41.7869')
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = requests.get(url)
        data = response.json()
        clima_atual = data.get('current_weather', {})
        
        return jsonify({
            "porto": "Macaé/RJ" if lat == '-22.3708' else "Outro Local",
            "temperatura_celsius": clima_atual.get('temperature'),
            "vento_kmh": clima_atual.get('windspeed'),
            "direcao_vento": clima_atual.get('winddirection')
        }), 200
    except Exception as e:
        return jsonify({"error": "Falha ao buscar dados climáticos", "details": str(e)}), 500

if __name__ == '__main__':
    # Roda em 0.0.0.0 para funcionar corretamente dentro do Docker
    app.run(host='0.0.0.0', port=5000, debug=True)