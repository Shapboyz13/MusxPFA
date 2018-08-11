from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os, sys
import urllib.error

import ytSearch
import py_yt as yt

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('xyz.html',songs=songs)

@app.route('/list', methods=['GET'])
def music():
    songs = os.listdir('static/music/')
    if(songs):
        return render_template('home.html',songs=songs)
        # return jsonify(songs)
    else:
        return jsonify(0)

@app.route('/search/', methods=['POST'])
def search_yt():
    if request.method == 'POST':
        search = request.form['search']
        print ("\n\n", "data:",search, "\n\n", file=sys.stdout)
        try:
            data=ytSearch.youtube_search(search);
            return render_template('download.html',songs=data)
        except urllib.error.HTTPError as e:
            print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


@app.route('/ret_streams', methods=['POST'])
def ret_streams():
    if(request.is_json):
        data=request.get_json()
        data = yt.ret_streams(data)
        return jsonify(data)
    else:
        return jsonify(0)

@app.route('/download', methods=['POST'])
def download():
    if(request.is_json):
        data=request.get_json()
        data = yt.download(data)
        return jsonify(data)
    else:
        return jsonify(0)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
