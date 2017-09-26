import sys
sys.dont_write_bytecode = True

from flask import Flask, request
from flask_restful import Resource, Api

from permutator import Permutator
from results import Results
from helper import formatResults
from dbadapter import DbAdapter

app = Flask(__name__)
api = Api(app)

db = DbAdapter()
permutator = Permutator(db)
results = Results(len(permutator.permutations))

class Reset(Resource):
    def get(self):
        db.cleanDatabase(false)
        if permutator.reset():
            return {'status': 'successful'}
        else:
            return {'status': 'failed'}

class GetNext(Resource):
    def get(self):
        return permutator.getNext()

class Results(Resource):
    def get(self):
        return formatResults(db.getBest(5))

@app.route('/return', methods=['GET', 'POST'])
def ReceiveData():
    content = request.json
    db.addEntry(content)
    return 'Successful'



api.add_resource(Reset, '/reset')
api.add_resource(GetNext, '/get_next')
api.add_resource(Results, '/results')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
