from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit,expr
from pyspark.sql.types import * # type: ignore
from pyspark import SparkFiles

from browser.utils import process_webdata
from browser.config import Config
import random
import string
if __name__ == "__main__":
    conf = Config()
    spark_conf = conf.spark_conf
    spark = SparkSession.builder \
        .config(conf=spark_conf) \
        .getOrCreate()

    schema = StructType([
        StructField("Profession", StringType()),
        StructField("Salary", StringType()),
        StructField("Company Name", StringType()),
        StructField("Location", StringType()),
        StructField("Start Date", StringType()),
        StructField("Telephone", StringType()),
        StructField("Email", StringType()),
        StructField("Job Description", StringType()),
        StructField("Ref.-Nr.", StringType()),  
        StructField("External Link", StringType()),
        StructField("Application Link", StringType())
        
    ])
    process_webdata(spark,schema)
