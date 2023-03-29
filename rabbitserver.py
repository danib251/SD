import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)

print("Starting Consuming")
channel.start_consuming()