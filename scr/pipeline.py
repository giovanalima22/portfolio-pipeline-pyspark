from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month, sum as spark_sum

RAW = "data/raw/orders.csv"
SILVER = "data/silver/orders"
GOLD = "data/gold/monthly_category"

spark = (
    SparkSession.builder
    .appName("PortfolioDataPipeline")
    .master("local[*]")
    .getOrCreate()
)

try:
    raw = spark.read.option("header", True).csv(RAW)

    silver = (
        raw
        .withColumn("order_id", col("order_id").cast("long"))
        .withColumn("customer_id", col("customer_id").cast("long"))
        .withColumn("product_id", col("product_id").cast("long"))
        .withColumn("quantity", col("quantity").cast("int"))
        .withColumn("unit_price", col("unit_price").cast("double"))
        .withColumn("order_date", to_date("order_date"))
        .filter(col("order_id").isNotNull())
        .filter(col("order_date").isNotNull())
        .filter(col("quantity") > 0)
        .filter(col("status") == "PAID")
        .dropDuplicates(["order_id"])
        .withColumn("revenue", col("quantity") * col("unit_price"))
        .withColumn("year", year("order_date"))
        .withColumn("month", month("order_date"))
    )

    silver.write.mode("overwrite").partitionBy("year", "month").parquet(SILVER)

    gold = (
        silver.groupBy("year", "month", "category")
        .agg(
            spark_sum("revenue").alias("revenue"),
            spark_sum("quantity").alias("items_sold"),
        )
        .orderBy("year", "month", "category")
    )

    gold.write.mode("overwrite").parquet(GOLD)

    print("Pipeline completed.")
    print("Silver:")
    silver.show(10, truncate=False)
    print("Gold:")
    gold.show(20, truncate=False)

finally:
    spark.stop()
