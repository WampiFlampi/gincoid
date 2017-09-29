from os import environ
import json

from flask import Flask, request, render_template, Response, redirect

app = Flask(__name__)

authorized = json.loads(
    environ['AUTHORIZED'])

force_https = (environ['FORCE_HTTPS'] == 'true')


@app.route('/')
def index():
    # redir to https
    if force_https:
        if request.url.startswith('http://'):
            return redirect(request.url.replace('http://', 'https://', 1), 301)

    # enforce auth
    authorized = False
    for user in authorized:
        if (request.authorization and
                user['usr'] == request.authorization.username and
                user['pass'] == request.authorization.password):
            authorized = True
            break
    if not authorized:
        return Response(
            'Could not verify access for URL', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return render_template('index.html')
