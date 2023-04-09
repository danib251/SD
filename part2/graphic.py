from flask import Flask, render_template
import time
import json
from queue import Queue

app = Flask(__name__, template_folder='templates')
datos = Queue()
datos_globales = []

class Graphic:
    def __init__(self, queue):
        self.queue = queue
        
    def process_data(self):
        print("Procesando datosasdzfsdhjgfhvsfdbjfvxzhjvf")
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                print(data)
                datos_globales.append(data)
            time.sleep(3)

@app.route('/')
def index():
    return render_template('index.html', datos=datos_globales)

@app.route('/data')
def data():
    return json.dumps(datos_globales)
    



        

    
