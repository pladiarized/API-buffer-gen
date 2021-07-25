from flask import Flask,jsonify,request
import requests
from urllib.parse import urlencode
from .config import app_config
from pymemcache.client import base

#import threading


def create_app(env_name):
    app = Flask(__name__)
    client = base.Client(('127.0.0.1', 6969))

    app.config.from_object(app_config[env_name])
    
    @app.route('/', methods=['GET'])
    def index():
        return jsonify(message="nah")

    @app.route('/setup')
    def main():
        length=1024
        global res
        res=[]
        type="uint16"
        endpoint = "https://qrng.anu.edu.au/API/jsonI.php"
        query_params = urlencode({"length" : length, "type" : type})
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url)
        if r.status_code in range(200,299):
            if res: #obsolete
                for i in range(len):
                    res.apprend(r.json()['data'][i])
                    return jsonify(message="updated", hehe="https://save418.com/")
            res=r.json()['data']
            return jsonify(message="ready", hehe="https://save418.com/")
    
    def update_response(res,len):
        type="uint16"
        endpoint = "https://qrng.anu.edu.au/API/jsonI.php"
        query_params = urlencode({"length" : len, "type" : type})
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url)
        if r.status_code in range(200,299):
            if res:
                for i in range(len):
                    res.append(r.json()['data'][i])
                    client.set('cached_res', res)
                    return jsonify(message="updated", hehe="https://save418.com/")

    @app.route('/result')
    def result():
        n = request.args['num']
        n = int(n)
        print(n)

        if n==0 or n is None or not res:
            main()
            if n==0:
                return jsonify(message="ready", hehe="https://save418.com/")
            if not res:
                return jsonify(message="created new cache memory. initially not present", hehe="https://save418.com/")
        
        #t = threading.Thread(target=update_response(res, n))
        #t.setDaemon(False)
        #t.start()
        res_string = ""
        for i in range(n):
            res_string+=str(res.pop())
        
        return jsonify(res_str = res_string, message="cool", hehe="https://save418.com/")

    return app