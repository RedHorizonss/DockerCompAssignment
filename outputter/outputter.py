#!/usr/bin/env python
import zlib
import json
import awkward as ak
import outputter_script as script
import konnections as kon
import pika
    
# Gets the samples dictionary
from infofile import samples

def callback(ch, method, properties, body):
    global num_of_processed_data, num_of_files_to_process
    
    # Decode information and show what was recieved
    decompressed_json = zlib.decompress(body)
    data_with_identifier = json.loads(decompressed_json)
    
    # Get the name of the data and the data itself
    data_name = data_with_identifier['data_name']
    data = data_with_identifier['data']
    
    # Make it an awkward array
    data = ak.from_iter(data)
    print(f" [x] Received data for {data_name}")
    
    # Add data to dictionary
    for category, s in samples.items():
        if data_name in s['list']:
            data_dict_key = category
            data_full[data_dict_key].append(data)  # Append data to the list

    num_of_processed_data += 1
    if num_of_processed_data == num_of_files_to_process:
        channel.stop_consuming()

connection = kon.rabbitmq_connection('rabbitmq')
channel = connection.channel()

channel.queue_declare(queue='data_output')

channel.basic_consume(queue='data_output',
                      auto_ack=True,
                      on_message_callback=callback)

print('OUTPUTTER: Connected to RabbitMQ')

# loops through dictionary an finds the number of data files to be processed
num_of_files_to_process = 0

for key, value in samples.items():
    num_of_files_to_process += len(value['list'])
    
num_of_processed_data = 0

# Creates dictionary to store data
data_full = {category: [] for category in samples}

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# Loop through data_full dictionary keys and concatenate lists to awkward arrays
for category, data_list in data_full.items():
    data_full[category] = ak.concatenate(data_list)

# Plot data
script.plot_data(data_full)

# Close connection
connection.close()