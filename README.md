# MyTest
Hello, this is my first task from an employer to test my knowledge, at this stage it took me about 1 day to complete.
The essence of this task is as follows.
The test application must connect to PostgreSQL or Redis and implement the following APIs:

1. Anagram check-takes two strings, and determines whether they are anagrams.  If they are, you need to increase the counter in Redis.   Returns JSON - whether they are anagrams and a counter from Redis.

2. Enter 10 devices in the database (the devices table), the type (dev_type) is determined randomly from the list: emeter, zigbee, lora, gsm. The dev_id field is a random 48 bits in hex format (MAC address). An endpoint (the endpoints table) must be bound to five of the added devices.  After recording, the HTTP status code 201 must be returned.

3. In the database, get a list of all devices that are not bound to the endpoint.  Return the number grouped by device type.

Example of a test.sql database.
