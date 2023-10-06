from flask import *
import threading
import os, sys

app = Flask(__name__)
class Dashboard:
    def __init__(self,parent):
        app.parent = parent
        self.thread = None
        self.run()
    def run(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.run()
    def _run(self):
        address = self.parent.config["dashboard"]["address"]
        app.run(host=address[0],port=address[1],debug=self.parent.config["debug"])
    @app.route("/")
    def index(action=""):
        return render_template("index.html")
    @app.route("/login")
    def index(action=""):
        
        return render_template("login.html")