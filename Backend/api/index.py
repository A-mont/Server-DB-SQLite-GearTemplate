from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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

# Crear la base de datos antes de arrancar la aplicación
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'Active Server'

@app.route('/player_status', methods=['POST'])
def player_status():
    try:
        # Obtener la información del cuerpo de la solicitud
        player_data = request.json

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

        return jsonify({'message': 'Información del jugador guardada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False)

