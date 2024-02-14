# Import necessary modules
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.String(50))
    message_body = db.Column(db.String(200))
    response = db.Column(db.String(200), nullable=True)

# Create database tables
db.create_all()

# Load messages from CSV file into the database
def load_messages_from_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            message = Message(
                userid=int(row['User ID']),  # Convert to integer
                timestamp=row['Timestamp (UTC)'],
                message_body=row['Message Body']
            )
            db.session.add(message)
    db.session.commit()

# Define a FlaskForm for sending messages
class SendMessageForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    message_body = StringField('Message Body', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# Define a FlaskForm for receiving messages
class ReceiveMessageForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    submit = SubmitField('Receive Messages')

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField('Search')

# Route for sending messages via web form
@app.route('/send_message', methods=['GET', 'POST'])
def send_message_form():
    form = SendMessageForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        message_body = form.message_body.data

        # Generate timestamp
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Create a new Message object and save it to the database
        message = Message(userid=user_id, message_body=message_body, timestamp=timestamp)
        db.session.add(message)
        db.session.commit()

        return redirect(url_for('agent_portal'))  # Redirect to agent portal after sending message
    return render_template('send_message_form.html', form=form)

# Route for receiving messages via web form
@app.route('/receive_message', methods=['GET', 'POST'])
def receive_message_form():
    form = ReceiveMessageForm()
    if form.validate_on_submit():
        user_id = form.user_id.data

        # Generate timestamp
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Query the database to retrieve messages for the specified user ID
        messages = Message.query.filter_by(userid=user_id).all()

        # Update each message with the current timestamp
        for message in messages:
            message.timestamp = timestamp
            db.session.commit()

        return render_template('receive_message_results.html', messages=messages)
    return render_template('receive_message_form.html', form=form)

# Endpoint to simulate receiving a message from a customer
@app.route('/api/message', methods=['GET', 'POST'])
def receive_message():
    message_data = request.json
    if message_data is None:
        return jsonify({'error': 'No JSON data received'}), 400

    if not all(key in message_data for key in ['user_id', 'message_body']):
        return jsonify({'error': 'Invalid message data format'}), 400

    # Extract data from message_data
    user_id = message_data['user_id']
    message_body = message_data['message_body']
    timestamp = message_data.get('timestamp')  # Optional field, if provided

    # Create a new Message object
    message = Message(userid=user_id, timestamp=timestamp, message_body=message_body)

    # Add the message to the database session and commit
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message received successfully'}), 201

# Define the endpoint for customers to send messages through the API
@app.route('/api/send_message', methods=['GET', 'POST'])
def send_message():
    # Extract JSON data from the request body
    message_data = request.json
    
    # Check if the request contains JSON data
    if not message_data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    # Check if the required fields are present in the message data
    if not all(key in message_data for key in ['user_id', 'message_body']):
        return jsonify({'error': 'Missing required fields in the request body'}), 400

    # Here you can implement the logic to send the message to the appropriate recipient(s)
    # For demonstration purposes, we'll just print the message to the console
    print("Sending message to user ID", message_data['user_id'])
    print("Message body:", message_data['message_body'])

    # Return a success response
    return jsonify({'message': 'Message sent successfully'}), 200

# Define the search_messages function
def search_messages(keyword):
    # Query the database to find messages containing the keyword
    messages = Message.query.filter(Message.message_body.ilike(f'%{keyword}%')).all()
    return messages

# Endpoint to display messages in the agent portal
@app.route('/agent/portal')
def agent_portal():
    if 'username' not in session:
        return redirect(url_for('login'))
    messages = Message.query.all()
    return render_template('agent_portal.html', messages=messages)

# Endpoint to respond to a message
@app.route('/respond/<int:message_id>', methods=['GET', 'POST'])
def respond_to_message(message_id):
    message = Message.query.get(message_id)
    message.response = request.form['response']
    db.session.commit()
    return "Response sent successfully", 200

# Endpoint to search messages
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()  # Assuming you have a SearchForm defined
    if request.method == 'POST':
        keyword = request.form['keyword']
        messages = search_messages(keyword)
        return render_template('search_results.html', messages=messages, form=form)
    return render_template('search.html', form=form)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('agent_portal'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists')
        else:
            # Create a new user and add it to the database
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    # Load messages from CSV file into the database
    load_messages_from_csv('customer_messages.csv')
    app.run(debug=True)
