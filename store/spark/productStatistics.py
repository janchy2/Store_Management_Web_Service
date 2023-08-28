from pyspark.sql import SparkSession, functions
import os

databaseUrl = os.environ["DATABASE_IP"]

builder = SparkSession.builder.appName("PySpark Application")
spark = builder.getOrCreate()

products_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{databaseUrl}:3306/store") \
    .option("dbtable", "store.products") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

orderproduct_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{databaseUrl}:3306/store") \
    .option("dbtable", "store.orderproduct") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

orders_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{databaseUrl}:3306/store") \
    .option("dbtable", "store.orders") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

rows = products_data_frame.join(orderproduct_data_frame, products_data_frame.id == orderproduct_data_frame.productId) \
    .join(orders_data_frame, orderproduct_data_frame.orderId == orders_data_frame.id) \
    .groupBy(products_data_frame.id, products_data_frame.name) \
    .agg(
    functions.sum(
        functions.when(orders_data_frame.status == "COMPLETE", orderproduct_data_frame.quantity)
        .otherwise(0)).alias("complete"),
    functions.sum(
        functions.when(orders_data_frame.status != "COMPLETE", orderproduct_data_frame.quantity)
        .otherwise(0)).alias("pending")).collect()

productList = []
for row in rows:
    object = {
        "name": row[1],
        "sold": int(row[2]),
        "waiting": int(row[3])
    }
    productList.append(object)

print("RESULT:")
print(productList)

spark.stop()
