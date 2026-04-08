# src/app.py
from flask import Flask, request, jsonify, render_template
import database

app = Flask(__name__)

# Garante que o banco de dados seja inicializado logo que a aplicação rodar
with app.app_context():
    database.init_db()

@app.route('/', methods=['GET'])
def index():
    """Painel principal com as últimas 10 leituras.""" # [cite: 141]
    leituras = database.listar_leituras(limite=10)
    
    if request.args.get('formato') == 'json': # [cite: 140]
        return jsonify(leituras)
    return render_template('index.html', leituras=leituras)

@app.route('/leituras', methods=['GET'])
def listar():
    """Histórico completo com paginação (limitado a 50 na função do DB por padrão).""" # [cite: 141]
    leituras = database.listar_leituras()
    
    if request.args.get('formato') == 'json': # [cite: 140]
        return jsonify(leituras)
    return render_template('historico.html', leituras=leituras)

@app.route('/leituras', methods=['POST'])
def criar():
    """Recebe o JSON do Arduino / simulador e insere no banco.""" # [cite: 141]
    dados = request.get_json() # [cite: 147]
    
    if not dados: # [cite: 148]
        return jsonify({'erro': 'JSON inválido'}), 400 # [cite: 149]
    
    try:
        # Pega a pressão se existir, senão usa None
        pressao = dados.get('pressao') # [cite: 154]
        id_novo = database.inserir_leitura( # [cite: 150]
            temperatura=dados['temperatura'], # [cite: 152]
            umidade=dados['umidade'], # [cite: 153]
            pressao=pressao
        )
        return jsonify({'id': id_novo, 'status': 'criado'}), 201 # [cite: 155]
    except KeyError:
        return jsonify({'erro': 'Faltam os campos obrigatorios (temperatura, umidade)'}), 400

@app.route('/leituras/<int:id>', methods=['GET'])
def detalhe(id):
    """Exibe uma leitura específica.""" # [cite: 141]
    leitura = database.buscar_leitura(id)
    if not leitura:
        return jsonify({'erro': 'Leitura nao encontrada'}), 404
        
    if request.args.get('formato') == 'json': # [cite: 140]
        return jsonify(leitura)
    return render_template('editar.html', leitura=leitura)

@app.route('/leituras/<int:id>', methods=['PUT'])
def atualizar(id):
    """Atualiza campos de uma leitura.""" # [cite: 141]
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400
        
    leitura_existente = database.buscar_leitura(id)
    if not leitura_existente:
        return jsonify({'erro': 'Leitura nao encontrada'}), 404
        
    database.atualizar_leitura(id, dados)
    return jsonify({'status': 'atualizado', 'id': id})

@app.route('/leituras/<int:id>', methods=['DELETE'])
def deletar(id):
    """Remove uma leitura do banco.""" # [cite: 141]
    leitura_existente = database.buscar_leitura(id)
    if not leitura_existente:
        return jsonify({'erro': 'Leitura nao encontrada'}), 404
        
    database.deletar_leitura(id)
    return jsonify({'status': 'deletado', 'id': id})

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    """Média, mín e máx do período.""" # [cite: 141]
    conn = database.get_db_connection()
    # Usando SQL nativo para calcular as estatísticas rapidamente
    query = '''
        SELECT 
            AVG(temperatura) as temp_media, MIN(temperatura) as temp_min, MAX(temperatura) as temp_max,
            AVG(umidade) as umid_media, MIN(umidade) as umid_min, MAX(umidade) as umid_max
        FROM leituras
    '''
    resultado = conn.execute(query).fetchone()
    conn.close()
    
    return jsonify(dict(resultado))

if __name__ == '__main__':
    # Usar modo debug apenas em desenvolvimento, conforme recomendado no PDF
    app.run(debug=True, host='0.0.0.0', port=5000) # [cite: 208]