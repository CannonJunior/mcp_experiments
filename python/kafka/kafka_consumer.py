# Copyright 2025 CannonJunior

# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.15
# By: CannonJunior with Google Gemini AI search results
# Prompt: kafka topic python
# Usage: uv run kafka_consumer.py
# Output (using kafka_producer.py): {'key': 'SuccessfulTest'}

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'my_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(message.value)
