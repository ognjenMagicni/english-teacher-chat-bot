from google import genai
import time
file = open('../application.yaml','r')
api = file.readline().split(" ")[1]

client = genai.Client(api_key=api)

from confluent_kafka import Consumer, Producer
conf = {'bootstrap.servers': 'localhost:9092',
            'group.id':f'group-{time.time()}',
            'auto.offset.reset': 'latest'}
consumer = Consumer(conf)
consumer.subscribe(["my_topic"])

conf = {
    'bootstrap.servers': 'localhost:9092',  # Change this if your Kafka is running elsewhere
    'client.id': 'python-producer'
}
producer = Producer(conf)



chat = client.chats.create(model="gemini-2.0-flash")
response = chat.send_message("You are english grammar teacher. You have several tasks. You will receive audio of a student and if necessary you have to correct him/her. Also you have to ask him/her some everyday questions. While providing response do not use markdown, just plain text and do not use new lines. Is that clear, do you need additional information?")
print(response.text)

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None: 
            continue
        else:
            audio = msg.value()
            file = open("audioSecond.mp3",'wb')
            file.write(audio)
            file.flush()
            file.close()
            audioUploaded = client.files.upload(file='audioSecond.mp3')
            response = chat.send_message(audioUploaded)
            print(response.text)
            producer.produce("bottopic", key="key", value=response.text)
            producer.poll(1)
finally:
    consumer.close()

        
