# Cassino

## TODO
* script which creates data structures
* add and remove players from the table
* transactions - money from players' accounts and to them
* checking accounts status
* adding money from outside

## Technologies
* Django Rest Framework
* Redis
* Lua scripts
* Transactions

## Instructions
* run docker with Redis <code>docker compose up --build</code>
* run redis <code>sudo docker run --name redis-stack -d -p 6379:6379 -p 8001:8001 -v "/Desktop/studia/adb/redis/data:/data" redis/redis-stack</code>

tips
go to 127.0.0.1