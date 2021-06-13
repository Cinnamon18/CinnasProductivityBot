# Just to shut up Azure lmao
from flask import Flask
# from threading import Thread

print("uwu\nuwu\nuwu\nuwu\nuwu\nuwu\nuwu\nuwu\n")

app = Flask(__name__)
app.run()
# def azureWhy():
# 	app.run(port=8000)
# thread = Thread(target=azureWhy)
# thread.start()
@app.route("/")
def hello():
    return "Hello, World!"