import flask
import uuid
import json
import os
import jsonschema

# location = os.path.dirname(os.path.abspath(__file__))
# CreateResourceSchema = json.load(open(os.path.join(location, 'schema', 'CreateResource.json')))
# GetResourceSchema = json.load(open(os.path.join(location, 'schema', 'GetResource.json')))
# SetResourceSchema = json.load(open(os.path.join(location, 'schema', 'SetResource.json')))

# def Validate(json, schema):
#     if not jsonschema.validate(json, schema):
#         raise Exception


class ResourceNotFoundException(Exception):
    pass

class Resources:
    def __init__(self):
        self.res: dict[str, str] = {}
    
    def CreateResource(self, initialValue: str = '') -> str:
        id = str(uuid.uuid4())
        self.res[id] = initialValue
        return id
    
    def UpdateResource(self, id: str, value: str):
        if not (id in self.res):
            raise ResourceNotFoundException()
        self.res[id] = value
    
    def GetResource(self, id: str) -> str:
        if not (id in self.res):
            raise ResourceNotFoundException()
        return id, self.res[id]

app = flask.Flask(__name__)
resources = Resources()

@app.route("/test/res", methods=['PUT'])
def AddResource():
    response = { 'id': resources.CreateResource() }
    return flask.make_response(response, 201)

@app.route("/test/res/<uuid:id>", methods=['GET'])
def GetResource(id: str):
    id, val = resources.GetResource(id.__str__())
    response = { 'val': val }
    return flask.make_response(response, 200)

@app.route("/test/res/<uuid:id>", methods=['POST'])
def UpdateResource(id: str):
    resources.UpdateResource(id.__str__(), flask.request.get_json()['val'])
    return flask.make_response('', 200)

@app.errorhandler(ResourceNotFoundException)
def HandleResourceNotFoundException(e):
    return 'Resource not found!', 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, ssl_context='adhoc')