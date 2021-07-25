from flask import Flask,jsonify,request
import requests
from urllib.parse import urlencode
from .config import app_config
from pymemcache.client import base

import threading


def create_app(env_name):
    app = Flask(__name__)
    client = base.Client(('localhost', 6969))

    app.config.from_object(app_config[env_name])
    
    @app.route('/', methods=['GET'])
    def index():
        return jsonify( message="ok")
    
    @app.route('/main/<length>')
    def main(length):
        res=[]
        type="uint16"
        endpoint = "https://qrng.anu.edu.au/API/jsonI.php"
        query_params = urlencode({"length" : length, "type" : type})
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url)
        if r.status_code in range(200,299):
            if res:
                for i in range(len):
                    res.apprend(r.json()['data'][i])
                    client.set('cached_res', res)
                    return jsonify(message="updated", hehe="https://save418.com/")

            client.set('cached_res', r.json()['data'])
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
                    res.apprend(r.json()['data'][i])
                    client.set('cached_res', res)
                    return jsonify(message="updated", hehe="https://save418.com/")

        if not res:
            main(res,len)

    app.route('/result')
    def result(n):
        n=request.args.get('n')

        res = client.get('cached_res')

        if n==0 or res is None:
            init_len = 1024
            res_list=[]
            main(res_list,init_len)
            if n==0:
                return jsonify(message="ready", hehe="https://save418.com/")
            if res is None:
                return jsonify(message="created new cache memory. initially not present", hehe="https://save418.com/")
        
        t = threading.Thread(target=update_response(), args=[res, n])
        t.setDaemon(False)
        t.start()
        res_string = ""
        for i in range(n):
            res_string+=str(res.pop())
        
        return jsonify(res_str = res_string, message="cool")




            

    
    return app