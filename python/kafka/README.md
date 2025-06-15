# PREREQUISITES
1. docker installed
$ sudo snap install docker
2. Kafka docker installed
$ sudo docker pull apache/kafka-native:4.0.0
3. Kafka docker container started:
$ sudo docker run -p 9092:9092 apache/kafka-native:4.0.0
4. python kafka installed
$ uv add kafka-python

# USAGE
1. uv run kafka_producer.py
2. uv run kafka_consumer.py
Standard output: {'key': 'SuccessfulTest'}
