from datetime import datetime
from gevent import pywsgi
from flask import Flask, render_template
app = Flask(__name__)

import dataManagement as db

#reference
# https://flask.palletsprojects.com/en/1.1.x/quickstart
# CSS -> https://www.w3schools.com/html/html_tables.asp 

manager = db.dataManagement()

@app.route('/', methods=['GET'])
def indexRoute():
    dataRequest = manager.getDataFromTable()
    return render_template('index.html',  data=dataRequest)


@app.route('/information/<int:id>', methods=['GET'])
def idRoute(id):
    dateNow = datetime.now().strftime("%Y-%m-%d, %H:%M:%S.%f'")
    manager.logRecord(dateNow,id)
    dataRequest = manager.getDataFromTable(id)
    return render_template('index.html',  data=dataRequest)
    
      

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET')
  return response

if __name__ == '__main__':
    server1 = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    server1.serve_forever()
    print("Server running")
