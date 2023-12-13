#!/usr/bin/env python
import worker_script as script
import json
import zlib
import awkward as ak
import konnections as kon
import pika

connection = kon.rabbitmq_connection('rabbitmq')
channel = connection.channel()

# Make queues for recieveing and sending data
channel.queue_declare(queue='data_input')
channel.queue_declare(queue='data_output')

print('WORKER: Connected to RabbitMQ')

# Set QoS to limit the number of unacknowledged messages to 1
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    # Decode information and show what was recieved
    body = body.decode('utf-8')
    print(f" [x] Received {body}")
    
    # Send needed information for script to get data
    prefix, sample = body.split(" ")
    data = script.read_file(prefix, sample)
    
    # Compress data with identifier to combine together in outputter and send to queue
    serialised_data = ak.to_list(data)
    data_with_identifier = {'data_name': sample, 'data': serialised_data}
    json_data = json.dumps(data_with_identifier)
    compressed_data = zlib.compress(json_data.encode('utf-8'))
    
    ch.basic_publish(exchange='',
                     routing_key='data_output',
                     body=compressed_data)
    
    print(f" [x] Sent data for {body}")

channel.basic_consume(queue='data_input',
                      auto_ack=False,
                      on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

