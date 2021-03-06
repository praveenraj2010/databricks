# Databricks notebook source
# MAGIC %md
# MAGIC #### Ingest drivers.json file

# COMMAND ----------

# MAGIC %run "../includes/configuration"

# COMMAND ----------

# MAGIC %run "../includes/common_functions"

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 1 - Read the JSON file using the spark dataframe reader API

# COMMAND ----------

from pyspark.sql.types import StructType,StructField,IntegerType,StringType,DateType

# COMMAND ----------

name_schema = StructType(fields = [
  StructField("forename", StringType(),True),
  StructField("surname", StringType(),True),
])

# COMMAND ----------

driver_schema = StructType(fields =[
  StructField ("driverId",IntegerType(),False),
  StructField ("driverRef",StringType(),True),
  StructField("number", IntegerType(),True),
  StructField ("code", StringType(),True),
  StructField ("name",name_schema),
  StructField ("dob",DateType()),
  StructField ("nationality", StringType(), True),
  StructField ("url", StringType(),True)
  
  
  
])

# COMMAND ----------

drivers_df= spark.read \
.schema(driver_schema) \
.json(f"{raw_folder_path}/drivers.json")


# COMMAND ----------

display(drivers_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 2 - Rename columns and add new columns 
# MAGIC 1. driverid renamed to driver_id
# MAGIC 2. driver Ref renamed to driver_ref
# MAGIC 3. ingestion date addedd 
# MAGIC 4. name added with concatenation of forename and surname

# COMMAND ----------

from pyspark.sql.functions import col, concat,current_timestamp,lit

# COMMAND ----------

drivers_with_ingestion_date_df = add_ingestion_date(drivers_df)

# COMMAND ----------

drivers_with_columns_df = drivers_with_ingestion_date_df.withColumnRenamed("driverId", "driver_id")\
                                    .withColumnRenamed("driverRef","driver_ref")\
                                    .withColumn("name",concat(col("name.forename"),lit(" "),col("name.surname")))

# COMMAND ----------

display(drivers_with_columns_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Step 3 - Drop unwanted columns
# MAGIC 1. name.forename
# MAGIC 2. name.surname
# MAGIC 3. url

# COMMAND ----------

drivers_final_df = drivers_with_columns_df.drop("url")

# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 4 - Write to processed container in parquet format

# COMMAND ----------

 drivers_final_df.write.mode("overwrite").parquet(f"{processed_folder_path}/drivers")

# COMMAND ----------

dbutils.notebook.exit("Success")
