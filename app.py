from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# In-memory user store
users = []

# Home route with form interface
@app.route('/', methods=['GET'])
def index():
    return render_template_string("""
        <h1>User Management API</h1>

        <h2>GET All Users</h2>
        <form action="/users" method="get">
            <button type="submit">Get All Users</button>
        </form>

        <h2>GET User by ID</h2>
        <form action="/users" method="get">
            <input name="id" placeholder="User ID" />
            <button type="submit">Get User</button>
        </form>

        <h2>POST Create User</h2>
        <form action="/users" method="post">
            <input name="name" placeholder="Name" />
            <input name="email" placeholder="Email" />
            <button type="submit">Create User</button>
        </form>

        <h2>PUT Update User</h2>
        <form action="/users/update" method="post">
            <input name="id" placeholder="User ID" />
            <input name="name" placeholder="New Name" />
            <input name="email" placeholder="New Email" />
            <button type="submit">Update User</button>
        </form>

        <h2>DELETE User</h2>
        <form action="/users/delete" method="post">
            <input name="id" placeholder="User ID" />
            <button type="submit">Delete User</button>
        </form>
    """)

# API: Get all users
@app.route('/users', methods=['GET'])
def get_users():
    user_id = request.args.get('id')
    if user_id:
        user = next((u for u in users if u['id'] == int(user_id)), None)
        if user:
            return jsonify(user), 200
        return jsonify({'message': 'User not found'}), 404
    return jsonify(users), 200

# API: Create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.form or request.get_json()
    user = {
        'id': len(users) + 1,
        'name': data.get('name'),
        'email': data.get('email')
    }
    users.append(user)
    return jsonify({'message': 'User created', 'user': user}), 201

# API: Update user
@app.route('/users/update', methods=['POST'])
def update_user():
    data = request.form or request.get_json()
    user_id = int(data.get('id'))
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    return jsonify({'message': 'User updated', 'user': user}), 200

# API: Delete user
@app.route('/users/delete', methods=['POST'])
def delete_user():
    data = request.form or request.get_json()
    user_id = int(data.get('id'))
    global users
    users = [u for u in users if u['id'] != user_id]
    return jsonify({'message': f'User with ID {user_id} deleted'}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
