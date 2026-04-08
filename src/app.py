from flask import Flask, request, jsonify, render_template
import database

app = Flask(__name__)

with app.app_context():
    database.init_db()

@app.route('/', methods=['GET'])
def index():
    """Painel principal com as últimas 10 leituras.""" 
    leituras = database.listar_leituras(limite=10)
    
    if request.args.get('formato') == 'json': 
        return jsonify(leituras)
    return render_template('index.html', leituras=leituras)

@app.route('/leituras', methods=['GET'])
def listar():
    """Histórico completo com paginação (limitado a 50 na função do DB por padrão).""" 
    leituras = database.listar_leituras()
    
    if request.args.get('formato') == 'json': 
        return jsonify(leituras)
    return render_template('historico.html', leituras=leituras)

@app.route('/leituras', methods=['POST'])
def criar():
    """Recebe o JSON do Arduino / simulador e insere no banco.""" 
    dados = request.get_json() 
    
    if not dados: 
        return jsonify({'erro': 'JSON inválido'}), 400 
    
    try:
        pressao = dados.get('pressao') 
        id_novo = database.inserir_leitura( 
            temperatura=dados['temperatura'],
            umidade=dados['umidade'], 
            pressao=pressao
        )
        return jsonify({'id': id_novo, 'status': 'criado'}), 201 
    except KeyError:
        return jsonify({'erro': 'Faltam os campos obrigatorios (temperatura, umidade)'}), 400

@app.route('/leituras/<int:id>', methods=['GET'])
def detalhe(id):
    """Exibe uma leitura específica.""" 
    leitura = database.buscar_leitura(id)
    if not leitura:
        return jsonify({'erro': 'Leitura nao encontrada'}), 404
        
    if request.args.get('formato') == 'json':
        return jsonify(leitura)
    return render_template('editar.html', leitura=leitura)

@app.route('/leituras/<int:id>', methods=['PUT'])
def atualizar(id):
    """Atualiza campos de uma leitura.""" 
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
    """Remove uma leitura do banco.""" 
    leitura_existente = database.buscar_leitura(id)
    if not leitura_existente:
        return jsonify({'erro': 'Leitura nao encontrada'}), 404
        
    database.deletar_leitura(id)
    return jsonify({'status': 'deletado', 'id': id})

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    """Média, mín e máx do período.""" 
    conn = database.get_db_connection()
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
    app.run(debug=True, host='0.0.0.0', port=5000) # [cite: 208]