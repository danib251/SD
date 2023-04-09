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
                datos_globales.append({"air_data_mean": data["air_data_mean"],
                       "co2_data_mean": data["co2_data_mean"],
                       "time": data["time"]})
                print(datos_globales)
            time.sleep(3)

@app.route('/')
def index():
    return render_template('index.html', datos=datos_globales)

@app.route('/data')
def data():
    return json.dumps(datos_globales) if datos_globales else "[]"
    



        

    
