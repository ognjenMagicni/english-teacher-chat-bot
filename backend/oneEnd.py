tema_send = "a"
tema_receive = "b"
import time
from confluent_kafka import Producer
conf1 = {
    'bootstrap.servers': 'localhost:9092',  
    'client.id': 'python-producer2'
}
from confluent_kafka import Consumer
conf2 = {'bootstrap.servers': 'localhost:9092',
        'group.id': 'id2',
        'auto.offset.reset': 'latest'}
producer = Producer(conf1)
consumer = Consumer(conf2)
consumer.subscribe([tema_receive])

i = 0
try:
    while True:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            else: 
                print("OneEnd: received:",msg.value().decode('utf-8'))
                break

        #message = input()
        producer.produce(tema_send, key="key", value=str(i))
        producer.poll(1)
        print("OneEnd: send: ",i)
        i+=-1
        

        time.sleep(10)
finally:
    consumer.close()





