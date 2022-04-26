
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import *
from sqlite_process_partition import process_partition

working_directory = 'jars/*'

spark = SparkSession \
    .builder \
    .appName("PySpark-UPSERT") \
    .config('spark.driver.extraClassPath', working_directory) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df_csv = spark \
    .read \
    .option("header", "true") \
    .csv("stocks_202204261909.csv")

df_csv.show(10, False)

df_csv.rdd.coalesce(10).foreachPartition(process_partition)

example = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:sqlite:example.db") \
    .option("dbtable", "stocks") \
    .load()

example.createOrReplaceTempView("stocks")

result = spark.sql("SELECT * FROM stocks")

result.show()
