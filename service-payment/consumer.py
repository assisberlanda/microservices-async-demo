import os
import pika
import json
import time

RABBIT_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

def process_payment(ch, method, properties, body):
    order_data = json.loads(body)
    print(f" [x] Iniciando pagamento do pedido: {order_data['order_id']}")
    
    # Simula o tempo de processamento bancário
    time.sleep(5) 
    
    print(f" [v] Pedido {order_data['order_id']} FINALIZADO!")
    # Confirma para o RabbitMQ que a mensagem foi processada
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
            channel = connection.channel()
            channel.queue_declare(queue='order_queue')

            channel.basic_consume(queue='order_queue', on_message_callback=process_payment)

            print(f' [*] Conectado ao RabbitMQ em {RABBIT_HOST}. Aguardando mensagens...')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print(" [!] RabbitMQ ainda não está pronto. Tentando em 5 segundos...")
            time.sleep(5)

if __name__ == '__main__':
    start_consumer()