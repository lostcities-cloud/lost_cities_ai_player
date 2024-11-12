#!/usr/bin/env python
import pika
import os

rabbitmq_url = os.environ.get('RABBITMQ_URL', 'localhost')
rabbitmq_queue = os.environ.get('RABBITMQ_QUEUE', 'ai-turn')


params = pika.ConnectionParameters(rabbitmq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

queue_declare(queue=rabbitmq_queue)

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)