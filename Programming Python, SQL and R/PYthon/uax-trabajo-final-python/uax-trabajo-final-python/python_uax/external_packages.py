


from flask import Flask, jsonify, request

# Create a Flask application instance
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/about')
def about():
    return 'About'

@app.route('/user/<int:user_id>')
def get_user(user_id):

    return f'User id: {user_id}'

if __name__ == '__main__':
    app.run(debug=True)
