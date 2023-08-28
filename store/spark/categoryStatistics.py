from pyspark.sql import SparkSession
import os

databaseUrl = os.environ["DATABASE_IP"]

builder = SparkSession.builder.appName("PySpark Application")
spark = builder.getOrCreate()

categories_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{databaseUrl}:3306/store") \
    .option("dbtable", "store.categories") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

productcategory_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{databaseUrl}:3306/store") \
    .option("dbtable", "store.productcategory") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

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

categories_data_frame.createOrReplaceTempView("categories")
productcategory_data_frame.createOrReplaceTempView("productcategory")
products_data_frame.createOrReplaceTempView("products")
orderproduct_data_frame.createOrReplaceTempView("orderproduct")
orders_data_frame.createOrReplaceTempView("orders")

query = """
            SELECT categories.name,
            SUM(CASE WHEN orders.status = 'COMPLETE' THEN orderproduct.quantity ELSE 0 END) AS completed
            FROM categories
            LEFT JOIN productcategory ON categories.id = productcategory.categoryId
            LEFT JOIN products ON products.id = productcategory.productId
            LEFT JOIN orderproduct ON products.id = orderproduct.productId
            LEFT JOIN orders ON orders.id = orderproduct.orderId
            GROUP BY categories.name
            ORDER BY completed DESC, categories.name ASC;
        """
rows = spark.sql(query).collect()

categoryList = []
for row in rows:
    categoryList.append(row[0])

print("RESULT:")
print(categoryList)

spark.stop()
