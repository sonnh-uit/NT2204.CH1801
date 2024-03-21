from flask import Flask, request, jsonify
import time
import subprocess
import database
# from urllib.parse import urlparse, parse_qs
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    # Get request method
    request_method = request.method
    headers = dict(request.headers)
    parameters = request.args.to_dict()
    response = {
        'server-hostname' : get_hostname(),
        'timestamp': int(time.time()),
        'course' : 'NT2204',
        'group_ID' : '10'
    }
    
    return jsonify(response)

@app.route('/api', methods=['GET'])
def api():
    action = request.args.get('action')
    query = request.args.get('query')
    query = urllib.parse.unquote(query)
    query = f"{query};"
    
    if action == 'create_table':
        status, result = database.create_table(query)
    elif action == 'insert_record':
        status, result = database.insert_record(query)
    elif action == 'select_records':
        status, result = database.select_records(query)
    else:
        status = 400
        result == "Query was denied"

    data = {
        'server-hostname' : get_hostname(),
        'timestamp': int(time.time()),
        'query_detail' : query,
        'status_code' : status,
        'message': result
    }
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def get_hostname() -> str:
    hostname_bytes  = subprocess.check_output('hostname', shell=True)
    hostname = hostname_bytes.decode('utf-8').strip()
    return hostname

if __name__ == '__main__':
    app.run(port=8080)