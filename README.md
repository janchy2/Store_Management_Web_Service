# Store_Management_Web_Service
The full description of the project requirements in Serbian is in the file IEP_PROJEKAT_2023.pdf. Following is the short description.
The goal is to create a store management system that includes neccessary web services, where each subpart of the system runs in its own Docker container. It is written mostly in Python, using Flask and SQLAlchemy. There are two main parts: authentication and store, each using its own MySql database.

Authentication web service is used for keeping track of the users. These are its functionalities:
- register customer
- register courier
- login (every user receives a JWT access token)
- delete (delets the account)

The store part is used for keeping track of the products, categories and orders. It is divided in three web services:
1) owner:
   - update (adds products from csv file)
   - product statistics (calculated using Spark cluster)
   - category statistics (calculated using Spark cluster)
2) customer:
   - search
   - order
   - status (gives the status of orders)
   - delivered (confirms delivery)
   - pay
3) courier:
   - orders to deliver
   - pick up order

It contains the file deployment.yaml, which allows the whole system to be started using Docker-compose.
Ethereum Blockchain is used to handle transactions in certain functionalities previously mentioned (order, delivered, pick up order and pay).

The tests folder contains evaluation tests for the project that were provided.
