from flask import Flask, render_template, request, redirect, url_for
import requests
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'

@app.route('/', methods=['POST'])
def create():
    error = ""
    id = request.form['id']
    value = request.form['value']
    if not id and not value:
        error = f"Create"
        url = "https://ec2-52-19-16-214.eu-west-1.compute.amazonaws.com:5555/test/res"
        response = requests.request("PUT", url, verify=False)
        id = response.json()['id']
    elif id and not value:
        error = f"Get - {id}"
        url = f"https://ec2-52-19-16-214.eu-west-1.compute.amazonaws.com:5555/test/res/{id}"
        response = requests.request("GET", url, verify=False)
        value = response.json()['val']
    elif id and value:
        error = f"Update - {id} - {value}"
        url = f"https://ec2-52-19-16-214.eu-west-1.compute.amazonaws.com:5555/test/res/{id}"
        response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=json.dumps({"val": value}), verify=False)
    else:
        error = "ERROR"
    return render_template('index.html', message=error, id=id, value=value)

@app.route('/', methods=['GET'])
def load():
    return render_template('index.html', message="")

 
if __name__=='__main__':
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')