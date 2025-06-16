# Copyright 2025 CannonJunior
  
# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.15
# By: CannonJunior with Google Gemini AI search results
# Prompt: kafka topic python
# Usage: uv run kafka_producer.py
# Output: none

from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer.send('my_topic', {'key': 'SuccessfulTest'})
producer.flush()
