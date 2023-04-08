import time
class Graphic:
    def __init__(self, queue):
        self.queue = queue
        
    def process_data(self):
        print("Procesando datosasdzfsdhjgfhvsfdbjfvxzhjvf")
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                print("info:", data)
            else:
                print("No hay datos")
            time.sleep(3)
    
