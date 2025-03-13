from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from confluent_kafka import Producer, Consumer
import time
import subprocess
conf = {
    'bootstrap.servers': 'localhost:9092',  # Change this if your Kafka is running elsewhere
    'client.id': 'python-producer'
}
producer = Producer(conf)

conf = {'bootstrap.servers': 'localhost:9092',
        'group.id': 'aa',
        'auto.offset.reset': 'smallest'}
consumer = Consumer(conf)
consumer.subscribe(["bottopic"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post('/runBot')
async def runBot():
    print("main.py runBot: started")
    script_name = "englishGrammarBot.py"
    with open("output.txt", "w") as stdout_file, open("error.txt", "w") as stderr_file:
        subprocess.Popen(
            ["python3", script_name],
            stdout=stdout_file,    #ne radi bas uvijek
            stderr=stderr_file
        )



@app.post("/sendAudio")
async def upload_audio(file: UploadFile = File(...)):
    consumer = Consumer(conf)
    consumer.subscribe(["bottopic"])
    print("main.py sendAudio: started")
    
    file_path = 'audio.mp3'

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())  


    audio_file = open('audio.mp3','rb')
    audio_bytes = audio_file.read()

    producer.produce("my_topic", key="key", value=audio_bytes)
    producer.poll(1)

    time_1 = time.time()
    while time.time()-time_1<=10:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        else:
            message = msg.value().decode('utf-8')
            consumer.close()
            return message
    consumer.close()
    print("main.py sendAudio: did not return anything")
        
    
        
