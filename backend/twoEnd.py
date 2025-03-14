tema_send = "b"
tema_receive = "a"
import time
from confluent_kafka import Producer
conf1 = {
    'bootstrap.servers': 'localhost:9092',  
    'client.id': 'python-producer1'
}
from confluent_kafka import Consumer
conf2 = {'bootstrap.servers': 'localhost:9092',
        'group.id': 'id',
        'auto.offset.reset': 'latest'}
producer = Producer(conf1)
consumer = Consumer(conf2)
consumer.subscribe([tema_receive])



i = 0
try:
    while True:
        #message = input()
        producer.produce(tema_send, key="key", value=str(i))
        producer.poll(1)
        print("TwoEnd: send:",i)
        i+=1
        

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            else: 
                print("TwoEnd: received:",msg.value().decode('utf-8'))
                break

        time.sleep(10)


        
finally:
    consumer.close()





