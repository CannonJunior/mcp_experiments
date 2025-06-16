Copyright 2025 CannonJunior
  
This file is part of mcp_experiments, and is released under the "MIT License Agreement".
Please see the LICENSE.md file that should have been included as part of this package.
Created: 2025.06.16
By: CannonJunior

## TODO
Ask Claude for a docker-compose for all dockers
- postgres with pgvector
- apache/kafka server
- kafka producer???

## postgres with pgvector
# Install
$ sudo docker pull pgvector/pgvector:pg16

# Run
$ sudo docker run -p 15432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=junior.cannon -e POSTGRES_DB=postgres --name $(whoami)_postgres --rm pgvector/pgvector:pg16 &

## Demonstration
1. Start kafka server
$ sudo docker run -p 9092:9092 apache/kafka-native:4.0.0
