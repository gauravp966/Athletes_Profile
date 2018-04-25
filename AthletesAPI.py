from flask import Flask
from flask import jsonify, request
from flask.ext.pymongo import PyMongo
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'athlete_profile'
app.config['MONGO_URI'] = 'mongodb://gauravp966:qwe123@ds257838.mlab.com:57838/athlete_profile'

mongo = PyMongo(app)

empDB = [
    {
        'id':'101',
        'name':'Gaurav',
        'title':'Software Engineer'
    },
    {
        'id':'201',
        'name':'consultadd',
        'title':'Inc'
    }
]


@app.route('/profiles',methods=['GET'])
def getAllEmp():
    profiles = mongo.db.athletes_info
    output = []
    for s in profiles.find():
        output.append({'name': s['name'], 'sports': s['sports'], 'nationality': s['nationality'], 'gender': s['gender']})
    return jsonify(output)


@app.route('/profile',methods=['POST'])
def create_emp():
    profiles = mongo.db.athletes_info
    name = request.json['name']
    sports = request.json['sports']
    nationality = request.json['nationality']
    gender = request.json['gender']

    profile_id = profiles.insert({'name': name, 'sports': sports, 'nationality': nationality, 'gender': gender})
    new_profile = profiles.find({'_id':profile_id})

    output = ({'name': new_profile['name'], 'sports': new_profile['sports'], 'nationality': new_profile['nationality'], 'gender': new_profile['gender']})
    return jsonify({'result': output})


@app.route('/empdb/<empID>',methods=['GET'])
def get_emp(empID):
    emp = [emp for emp in empDB if emp['id'] == empID]
    return jsonify({'emps':emp})


@app.route('/empdb/<empID>',methods=['PUT'])
def update_emp(empID):
    emp = [emp for emp in empDB if emp['id'] == empID]
    if 'name' in request.json:
        emp[0]['name'] = request.json['name']
    if 'title' in request.json:
        emp[0]['title'] = request.json['title']
    return jsonify({'emps':emp})

@app.route('/empdb/<empID>',methods=['DELETE'])
def delete_emp(empID):
    emp = [emp for emp in empDB if emp['id'] == empID]
    empDB.remove(emp[0])
    return jsonify({'response':'Success'})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
