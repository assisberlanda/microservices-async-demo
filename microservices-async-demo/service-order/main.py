import os
import json
import pika
from fastapi import FastAPI

app = FastAPI()

# Configuração via variável de ambiente (definida no docker-compose.yml)
RABBIT_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

def get_rabbitmq_connection():
    # Tenta conectar ao broker
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))

@app.post("/orders")
async def create_order(order_id: int, item: str):
    order = {"order_id": order_id, "item": item, "status": "PENDING"}
    
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue='order_queue')
        
        channel.basic_publish(
            exchange='',
            routing_key='order_queue',
            body=json.dumps(order)
        )
        connection.close()
        return {"message": "Evento publicado com sucesso", "order": order}
    except Exception as e:
        return {"error": f"Falha ao conectar ao RabbitMQ: {str(e)}"}

@app.get("/orders")
async def list_orders():
    # Em um cenário real, você buscaria no banco de dados
    return {"message": "Lista de pedidos (Mock)", "data": []}