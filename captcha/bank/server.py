from flask import Flask, request, jsonify, render_template, redirect, cli
from datetime import datetime
import time, threading, logging

tokens = []


def manageTokens():
    while True:
        for token in tokens:
            if token['expiry'] < datetime.now().timestamp():
                tokens.remove(token)

        time.sleep(5)

cli.show_server_banner = lambda *_: None
app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/api/submit', methods=['POST'])
def submit():
    try:
        token = request.form['token']
        sitekey = request.form['sitekey']
        expiry = datetime.now().timestamp() + 115
        tokenDict = {
            'token': token,
            'expiry':expiry,
            'sitekey':sitekey
        }
        tokens.append(tokenDict)
        return jsonify({
            'success':True,
            'error':None,
            'result':'Token harvested and stored'
        })
    except Exception as e:
        return jsonify({
            'success':False,
            'error':'Unknown error',
            'result':None
        })

@app.route('/api/count')
def api_count():
    return jsonify({
        'success':True,
        'error':None,
        'result':len(tokens)
    })
        
@app.route('/api/token')
def api_fetch_token():
    try:
        sitekey = request.form['sitekey']

        for token in tokens:
            if token['sitekey'] == sitekey:
                tokenData = token
                tokens.remove(token)
                return jsonify({
                    'success': True, 
                    'error': None,
                    'result': tokenData
                })

        return jsonify({
            'success': False,
            'error': 'Token requested but none available',
            'result': None
        })

    except:
        return jsonify({
            'success': False,
            'error': 'Token requested but none available',
            'result': None
        })

@app.route('/')
def hello():
    return 'Hello!'

def startServer():
    threading.Thread(target=manageTokens).start()
    app.run()
