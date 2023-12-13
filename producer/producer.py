import producer_script as script
import konnections as kon
import pika

# Function to send file names to the queue
def send_file_names():
    prefix_val_list = script.get_data_from_files()
    for prefix_val in prefix_val_list:
        
        channel.basic_publish(exchange='',
                            routing_key='data_input',
                            body=prefix_val)
        
        print(f" [x] Sent {prefix_val}")
    
# Connects to rabbit to send file names
connection = kon.rabbitmq_connection('rabbitmq')
channel = connection.channel()

channel.queue_declare(queue='data_input')

print('PRODUCER: Connected to RabbitMQ')

send_file_names()

print("Sent everything to be processsed.")
connection.close()