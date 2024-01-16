from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    wallet = db.Column(db.String(50), unique=True)  
    connected = db.Column(db.Boolean, default=False)  

# Crear la base de datos 
with app.app_context():
    db.create_all()
    
vector_list = []


csv_file_path = './players.csv'

@app.route('/')
def home():
    return 'Active Server'

@app.route('/player_status', methods=['POST'])
def player_status():
    try:
        # Obtener la información del cuerpo de la solicitud
        player_data = request.json
        
        
        print("Aqui estoy", request.json)

        # Obtener la dirección de la wallet del jugador
        wallet_address = player_data.get('wallet')

        # Verificar si el jugador ya existe en la base de datos
        with app.app_context():
            player = Player.query.filter_by(wallet=wallet_address).first()

        if player:
            # Si el jugador ya existe, actualizar su información
            with app.app_context():
                player.name = player_data.get('name')
                player.connected = player_data.get('connected', False)  # Establecer el estado de conexión
        else:
            # Si el jugador no existe, crear uno nuevo
            with app.app_context():
                new_player = Player(
                    name=player_data.get('name'),
                    wallet=wallet_address,
                    connected=player_data.get('connected', False)
                )
                db.session.add(new_player)

        # Guardar los cambios en la base de datos
        with app.app_context():
            db.session.commit()
            print('Información del jugador guardada correctamente en la base de datos')

        return jsonify({"Player": player_data})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/players', methods=['GET'])
def get_players():
    try:
        print("Antes de la consulta a la base de datos")
        # Obtener la información de todos los jugadores en la base de datos
        with app.app_context():
            players = Player.query.all()
            print("Después de la consulta a la base de datos")

            player_list = [{'id': player.id, 'name': player.name, 'wallet': player.wallet, 'connected': player.connected} for player in players]
        
            print(player_list)
        return jsonify({'players': player_list})
    except Exception as e:
        print("Error en la ruta /players:", str(e))
        return jsonify({'error': str(e)})
    
    
@app.route('/csv_status', methods=['POST'])
def csv_status():
    try:
        player_data = request.json
        csv_data = [player_data.get('id'), player_data.get('name'), player_data.get('wallet'), player_data.get('connected')]

        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_data)

        return jsonify({'message': 'Información del jugador guardada en el archivo CSV'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
    
    
@app.route('/vector_status', methods=['POST'])
def vector_status():
    try:
        player_data = request.json
      
        vector_data = {'id': player_data.get('id'), 'name': player_data.get('name'), 'wallet': player_data.get('wallet'), 'connected': player_data.get('connected')}
        
        vector_list.append(vector_data)
        
        print(vector_list)

        return jsonify({'message': 'Información del jugador almacenada en el vector'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

