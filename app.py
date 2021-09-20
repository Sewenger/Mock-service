from flask import Flask, request
import json
import datetime
from faker import Faker

app = Flask(__name__)

USERS = [
    {'id': 1,
     'name': 'John',
     'job': 'qa',
     'createdAt': '2021-09-21T00:02:34.616540'},
    {'id': 2,
     'name': 'Mick',
     'job': 'qa',
     'createdAt': '2021-09-21T00:01:34.616540'},
    {'id': 3,
     'name': 'Leon',
     'job': 'qa',
     'createdAt': '2021-09-21T00:00:34.616540'},
]


@app.route('/api/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if not data.get('name'):
            return {'msg': 'Name field is required'}, 400
        if not data.get('job'):
            return {'msg': 'Job field is required'}, 400
        max_id = max(USERS, key=lambda x: x['id'])
        data['id'] = max_id['id'] + 1
        data['createdAt'] = datetime.datetime.now().isoformat()
        USERS.append(data)
        return data, 201
    else:
        return {
            'count': len(USERS),
            'data': USERS
        }


@app.route('/api/users/<int:id>')
def user_id(id):
    if users := tuple(filter(lambda x: x['id'] == id, USERS)):
        return users[0]
    return {'msg': 'User not found'}, 404


@app.route('/api/users/<int:id>/random')
def user_id_random(id):
    faker = Faker()
    return {'id': id,
            'name': faker.first_name(),
            'job': faker.job(),
            'createdAt': faker.date_time().isoformat()}


if __name__ == '__main__':
    app.debug = True
    app.run()
