# Copyright 2025 CannonJunior
  
# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.15
# By: CannonJunior with Claude (3.7 free version)
# Prompt): Write a Python MCP server with FastMCP. The server's tool should reads json data from a KafkaConsumer.
# Usage: invoked by a FastMCP python client

#!/usr/bin/env python3
"""
Kafka MCP Server using FastMCP
Provides tools to consume JSON messages from Kafka topics
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import signal
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global consumer storage
active_consumers: Dict[str, KafkaConsumer] = {}

class KafkaConsumerManager:
    def __init__(self):
        self.consumers = {}
        self.running = True
    
    def create_consumer(self, topic: str, bootstrap_servers: str = "localhost:9092", 
                       group_id: str = "mcp-consumer", **kwargs) -> KafkaConsumer:
        """Create a new Kafka consumer"""
        consumer_config = {
            'bootstrap_servers': bootstrap_servers.split(','),
            'group_id': group_id,
            'auto_offset_reset': 'latest',
            'enable_auto_commit': True,
            'value_deserializer': lambda x: json.loads(x.decode('utf-8')) if x else None,
            'key_deserializer': lambda x: x.decode('utf-8') if x else None,
            **kwargs
        }
        
        try:
            consumer = KafkaConsumer(topic, **consumer_config)
            consumer_key = f"{topic}:{group_id}"
            self.consumers[consumer_key] = consumer
            logger.info(f"Created Kafka consumer for topic '{topic}' with group_id '{group_id}'")
            return consumer
        except Exception as e:
            logger.error(f"Failed to create Kafka consumer: {e}")
            raise
    
    def get_consumer(self, topic: str, group_id: str = "mcp-consumer") -> Optional[KafkaConsumer]:
        """Get existing consumer or None"""
        consumer_key = f"{topic}:{group_id}"
        return self.consumers.get(consumer_key)
    
    def close_consumer(self, topic: str, group_id: str = "mcp-consumer"):
        """Close a specific consumer"""
        consumer_key = f"{topic}:{group_id}"
        if consumer_key in self.consumers:
            self.consumers[consumer_key].close()
            del self.consumers[consumer_key]
            logger.info(f"Closed consumer for topic '{topic}' with group_id '{group_id}'")
    
    def close_all_consumers(self):
        """Close all consumers"""
        for consumer in self.consumers.values():
            try:
                consumer.close()
            except Exception as e:
                logger.error(f"Error closing consumer: {e}")
        self.consumers.clear()
        logger.info("Closed all Kafka consumers")

# Initialize the consumer manager
kafka_manager = KafkaConsumerManager()

# Initialize FastMCP server
mcp = FastMCP("Kafka Consumer Server")

@mcp.tool("kafka_consume_messages")
async def kafka_consume_messages(
    topic: str,
    bootstrap_servers: str = "localhost:9092",
    group_id: str = "mcp-consumer",
    timeout_ms: int = 5000,
    max_messages: int = 10
) -> List[Dict[str, Any]]:
    """
    Consume JSON messages from a Kafka topic
    
    Args:
        topic: Kafka topic name to consume from
        bootstrap_servers: Comma-separated list of Kafka brokers (default: localhost:9092)
        group_id: Consumer group ID (default: mcp-consumer)
        timeout_ms: Timeout in milliseconds for polling (default: 5000)
        max_messages: Maximum number of messages to consume (default: 10)
    
    Returns:
        List of consumed messages with metadata
    """
    try:
        # Get or create consumer
        consumer = kafka_manager.get_consumer(topic, group_id)
        if not consumer:
            consumer = kafka_manager.create_consumer(
                topic=topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id
            )
        
        messages = []
        
        # Poll for messages
        logger.info(f"Polling messages from topic '{topic}' (timeout: {timeout_ms}ms, max: {max_messages})")
        
        message_records = consumer.poll(timeout_ms=timeout_ms, max_records=max_messages)
        
        for topic_partition, records in message_records.items():
            for record in records:
                message_data = {
                    "topic": record.topic,
                    "partition": record.partition,
                    "offset": record.offset,
                    "key": record.key,
                    "value": record.value,
                    "timestamp": datetime.fromtimestamp(record.timestamp / 1000).isoformat() if record.timestamp else None,
                    "timestamp_type": record.timestamp_type,
                    "headers": dict(record.headers) if record.headers else {}
                }
                messages.append(message_data)
        
        logger.info(f"Consumed {len(messages)} messages from topic '{topic}'")
        return messages
        
    except json.JSONDecodeError as e:
        error_msg = f"Failed to decode JSON message: {e}"
        logger.error(error_msg)
        return [{"error": error_msg}]
    except KafkaError as e:
        error_msg = f"Kafka error: {e}"
        logger.error(error_msg)
        return [{"error": error_msg}]
    except Exception as e:
        error_msg = f"Unexpected error consuming messages: {e}"
        logger.error(error_msg)
        return [{"error": error_msg}]

@mcp.tool("kafka_peek_messages")
async def kafka_peek_messages(
    topic: str,
    bootstrap_servers: str = "localhost:9092",
    group_id: str = "mcp-peek-consumer",
    partition: int = 0,
    offset: str = "latest",
    max_messages: int = 5
) -> List[Dict[str, Any]]:
    """
    Peek at messages from a specific partition without committing offsets
    
    Args:
        topic: Kafka topic name
        bootstrap_servers: Comma-separated list of Kafka brokers
        group_id: Consumer group ID for peeking
        partition: Partition number to peek from (default: 0)
        offset: Offset position ('earliest', 'latest', or specific number)
        max_messages: Maximum number of messages to peek (default: 5)
    
    Returns:
        List of peeked messages with metadata
    """
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers.split(','),
            group_id=group_id,
            enable_auto_commit=False,  # Don't commit offsets when peeking
            value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None,
            key_deserializer=lambda x: x.decode('utf-8') if x else None
        )
        
        from kafka import TopicPartition
        tp = TopicPartition(topic, partition)
        consumer.assign([tp])
        
        # Seek to the desired offset
        if offset == "earliest":
            consumer.seek_to_beginning(tp)
        elif offset == "latest":
            consumer.seek_to_end(tp)
        else:
            try:
                consumer.seek(tp, int(offset))
            except ValueError:
                consumer.seek_to_end(tp)
        
        messages = []
        records = consumer.poll(timeout_ms=5000, max_records=max_messages)
        
        for topic_partition, record_list in records.items():
            for record in record_list:
                message_data = {
                    "topic": record.topic,
                    "partition": record.partition,
                    "offset": record.offset,
                    "key": record.key,
                    "value": record.value,
                    "timestamp": datetime.fromtimestamp(record.timestamp / 1000).isoformat() if record.timestamp else None,
                    "headers": dict(record.headers) if record.headers else {}
                }
                messages.append(message_data)
        
        consumer.close()
        logger.info(f"Peeked {len(messages)} messages from topic '{topic}' partition {partition}")
        return messages
        
    except Exception as e:
        error_msg = f"Error peeking messages: {e}"
        logger.error(error_msg)
        return [{"error": error_msg}]

@mcp.tool("kafka_list_topics")
async def kafka_list_topics(bootstrap_servers: str = "localhost:9092") -> Dict[str, Any]:
    """
    List available Kafka topics
    
    Args:
        bootstrap_servers: Comma-separated list of Kafka brokers
    
    Returns:
        Dictionary with topic information
    """
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers.split(','),
            group_id='mcp-topic-lister'
        )
        
        # Get topic metadata
        topics = consumer.topics()
        topic_details = {}
        
        for topic in topics:
            partitions = consumer.partitions_for_topic(topic)
            topic_details[topic] = {
                "partition_count": len(partitions) if partitions else 0,
                "partitions": list(partitions) if partitions else []
            }
        
        consumer.close()
        
        result = {
            "topics": list(topics),
            "topic_count": len(topics),
            "topic_details": topic_details
        }
        
        logger.info(f"Listed {len(topics)} Kafka topics")
        return result
        
    except Exception as e:
        error_msg = f"Error listing topics: {e}"
        logger.error(error_msg)
        return {"error": error_msg}

@mcp.tool("kafka_close_consumer")
async def kafka_close_consumer(
    topic: str,
    group_id: str = "mcp-consumer"
) -> Dict[str, str]:
    """
    Close a specific Kafka consumer
    
    Args:
        topic: Topic name of the consumer to close
        group_id: Consumer group ID to close
    
    Returns:
        Status message
    """
    try:
        kafka_manager.close_consumer(topic, group_id)
        return {"status": "success", "message": f"Closed consumer for topic '{topic}' with group_id '{group_id}'"}
    except Exception as e:
        error_msg = f"Error closing consumer: {e}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}

@mcp.resource("kafka://config")
async def kafka_config_resource():
    """Get current Kafka configuration and active consumers"""
    active_consumers_info = {}
    for key, consumer in kafka_manager.consumers.items():
        topic, group_id = key.split(':', 1)
        active_consumers_info[key] = {
            "topic": topic,
            "group_id": group_id,
            "bootstrap_servers": consumer.config.get('bootstrap_servers', [])
        }
    
    return {
        "active_consumers": active_consumers_info,
        "consumer_count": len(kafka_manager.consumers)
    }

@mcp.prompt("kafka_usage")
async def kafka_usage_prompt():
    """Generate usage instructions for the Kafka MCP server"""
    return """This Kafka MCP server provides tools to consume JSON messages from Kafka topics:

Available tools:
1. kafka_consume_messages - Consume messages from a topic
2. kafka_peek_messages - Peek at messages without committing offsets  
3. kafka_list_topics - List available Kafka topics
4. kafka_close_consumer - Close a specific consumer

Example usage:
- Consume from topic: kafka_consume_messages(topic="my-topic", max_messages=5)
- Peek latest messages: kafka_peek_messages(topic="my-topic", offset="latest")
- List topics: kafka_list_topics(bootstrap_servers="localhost:9092")

The server automatically manages consumer connections and handles JSON deserialization."""

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal, closing consumers...")
    kafka_manager.close_all_consumers()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("Starting Kafka MCP Server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    finally:
        kafka_manager.close_all_consumers()
        logger.info("Kafka MCP Server stopped")
