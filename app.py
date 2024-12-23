from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy # type: ignore
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database model for messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create the database
db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    # Process the contact form (e.g., save to database or send email)
    return jsonify({'status': 'Message received, thank you!'}), 200

@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    username = data.get('username', 'Anonymous')
    message = data.get('message', '')

    # Save message to the database
    new_message = Message(username=username, message=message)
    db.session.add(new_message)
    db.session.commit()

    # Broadcast the message to all clients
    send({'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
