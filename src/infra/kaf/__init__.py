from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer('my_favorite_topic')
producer = KafkaProducer()

for msg in consumer:
    print (msg)
