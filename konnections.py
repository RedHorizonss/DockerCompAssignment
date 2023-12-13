import pika
import time

def rabbitmq_connection(host, retries=10, delay=5):
    for _ in range(retries):
        try:
            return pika.BlockingConnection(pika.ConnectionParameters(host=host))
        
        except pika.exceptions.AMQPConnectionError:
            
            print(f"Retrying to connnect in {delay} seconds...")
            time.sleep(delay)
            
    raise Exception(f"Could not connenct to RabbitMQ after {retries} retries.")