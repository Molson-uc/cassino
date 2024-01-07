# Cassino API

## Technologies

- Django Rest Framework
- Redis
- Lua scripts
- Transactions
- Docker

## Instructions

To use the Cassino API, follow these steps:

1. Run Docker Compose:
   <code>docker-compose up</code>

2. Set data in the database:
   <code>python script.py</code>

## Introduction

The Cassino API is designed for handling token transactions in a web casino. The project prioritizes high performance, utilizing Redis as the database for efficient transaction management.

Supported functions include:

- Creating/Deleting game tables
- Creating/Deleting players for tables
- Token transactions
- Purchasing of tokens
