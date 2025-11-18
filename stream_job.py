from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum, avg
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType

# 1. Initialize Spark with Dynamic Allocation Configs
# These configs allow the cluster to scale up/down based on load
spark = (
    SparkSession.builder.appName("CS_Student_Autoscaling_ETL")
    .config("spark.dynamicAllocation.enabled", "true")
    .config("spark.dynamicAllocation.shuffleTracking.enabled", "true")
    .config("spark.dynamicAllocation.minExecutors", "1")
    .config("spark.dynamicAllocation.maxExecutors", "10")
    .config("spark.sql.shuffle.partitions", 5)
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# 2. Define New Schema (Matches the CS Student Data)
schema = (
    StructType()
    .add("timestamp", DoubleType())
    .add("student_id", StringType())
    .add("student_name", StringType())
    .add("course", StringType())
    .add("activity", StringType())
    .add("tool_used", StringType())
    .add("lines_of_code", IntegerType())
    .add("last_error", StringType())
    .add("cpu_usage_pct", DoubleType())
)

# 3. Read from Kafka
# Note: Updated topic to 'cs_student_logs'
kafka_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "cs_student_logs")
    .option("startingOffsets", "latest")
    .load()
)

# 4. Parse JSON & ETL
# - Cast binary value to String
# - Parse JSON using the schema
# - Convert the float timestamp to a TimestampType for Windowing
parsed_df = (
    kafka_df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
    .withColumn("event_time", col("timestamp").cast("timestamp"))
)

# 5. Window Aggregation
# Logic: Every 10 seconds, calculate:
#   - Total Lines of Code written
#   - Average CPU Usage
#   - Grouped by Course and Activity
windowed_aggs = (
    parsed_df.withWatermark("event_time", "1 minute")
    .groupBy(window(col("event_time"), "10 seconds"), col("course"), col("activity"))
    .agg(sum("lines_of_code").alias("total_loc"), avg("cpu_usage_pct").alias("avg_cpu"))
)

# 6. Write to Console
# Using 'update' mode so we see the aggregates update as new data flows in
query = (
    windowed_aggs.writeStream.outputMode("update")
    .format("console")
    .option("truncate", "false")
    .trigger(processingTime="5 seconds")
    .start()
)

query.awaitTermination()
