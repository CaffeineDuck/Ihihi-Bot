from flask import Flask
from threading import Thread
import random


app = Flask(__name__)

@app.route('/')
def home():
	return 'Im in!'

def run():
  app.run()

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()