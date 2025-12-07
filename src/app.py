from flask import Flask, request, jsonify
from db import init_db, get_users, create_user as db_create_user

app = Flask(__name__)

app.config['DATABASE'] = 'urfu2025.db'
init_db(app.config['DATABASE'])


@app.route('/', methods=['GET'])
def hello():
    return 'Hello URFU'

@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.json

        if not data or 'name' not in data:
            return jsonify({'error': 'Имя не найдено'}), 400

        user_id = db_create_user(app.config['DATABASE'], data['name'], data.get('email', ''))
        return jsonify({
            'message': 'Пользователь успешно создан',
            'id': user_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users', methods=['GET'])
def list_users():
    users = get_users(app.config['DATABASE'])
    return jsonify([dict(user) for user in users])


if __name__ == '__main__':
    app.run(debug=True)