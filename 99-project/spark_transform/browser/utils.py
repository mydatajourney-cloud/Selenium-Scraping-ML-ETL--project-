from pyspark.sql.functions import udf, to_timestamp, date_trunc
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit,expr, when, sha2, concat_ws
import pyspark.sql.functions as F

from pyspark.sql.types import *
import re
import psycopg2
from pyspark import SparkFiles
from psycopg2.extras import execute_values


from pyspark.sql.functions import (
    col, date_format, to_date, hour, dayofweek, month, year)


def write_df_to_postgres(df, table_name,schema_name,id):
    pandas_df = df.toPandas()

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="project-07",
        user="postgres",
        password="admin",
        host="host.docker.internal",
        port=5432
    )
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO public.{table} {schema}
        VALUES %s
        ON CONFLICT ({primary_key}) DO NOTHING;
    """.format(table=table_name, schema=schema_name, primary_key=id)

    records = pandas_df.to_records(index=False).tolist()
    execute_values(cursor, insert_sql, records)
    conn.commit()
    cursor.close()
    conn.close()

salary_schema = StructType([
    StructField("paytime_part", StringType(), True),
    StructField("min_salary", DoubleType(), True),
    StructField("max_salary", DoubleType(), True),
    StructField("unit_part", StringType(), True)
])

@udf(returnType=salary_schema)
def parse_salary(s):
    if s == None or s == "":
        return {
        "paytime_part": "",
        "min_salary": 0,
        "max_salary": 0,
        "unit_part": ""
    }

    
    parts = s.split("/")
    left_part = parts[0].strip() if len(parts) > 0 else ""
    paytime_part = parts[1].strip() if len(parts) > 1 else ""

    min_salary, max_salary, unit_part = None, None, ""

    try:
        salary_parts = left_part.split()
        # Ví dụ: "200 $ - 300 $"
        if "-" in left_part:
            if len(salary_parts) >= 4:
                min_salary = float(salary_parts[0])
                max_salary = float(salary_parts[3])
                unit_part = salary_parts[1]
        else:
            if len(salary_parts) >= 2:
                min_salary = float(salary_parts[0])
                max_salary = float(salary_parts[0])
                unit_part = salary_parts[1]
    except Exception:
        print("Xảy ra lỗi ở khi xử lý salary")
        pass

    return {
        "paytime_part": paytime_part,
        "min_salary": min_salary,
        "max_salary": max_salary,
        "unit_part": unit_part
    }





# --- Hàm xử lý DataFrame ---
def process_webdata(spark, data_schema):
    df = spark.read.option("header", True).option("sep", "|").option("quote", '"').option("escape", '"').option("multiLine", True).csv("s3a://project-06-vtdatalake/raw_data/jobs_data_1.csv")
    # Transform Company Name
    df = df.withColumn(
        "Company Name",
        F.regexp_replace(F.col("Company Name"), "Arbeitgeber:", "")
    )
    df = df.withColumn(
        "Company Name",
        F.translate(F.col("Company Name"), "\n\r", "")
    )
    # Transform Email
    df = df.withColumn(
        "emails_array",
        when(F.col("Email").isNull(), F.array().cast("array<string>"))
        .otherwise(F.expr("split(regexp_replace(Email, \"'|\\[|\\]\", ''), ', ')"))
    )
    df = df.withColumn(
        "Email",
        F.concat_ws(", ", F.array_distinct(F.col("emails_array")))
    )

    # Transform Start Date
    df = df.withColumn(
        "Start Date",
        F.regexp_replace(F.col("Start Date"), "Beginn ab ", "")
    )
    df = df.withColumn(
        "Start Date",
        when(col("Start Date").isNull(), lit(None).cast("date"))
        .otherwise(F.to_date("Start Date", "dd.MM.yyyy"))
    )

    # Transform Salary
    df = df.withColumn("Salary", parse_salary("Salary"))

    # Chọn và rename các cột
    df = df.select(
        col("Profession").alias("profession"),
        col("Salary.min_salary").alias("salary_min"),
        col("Salary.max_salary").alias("salary_max"),
        col("Salary.unit_part").alias("salary_unit"),
        col("Salary.paytime_part").alias("salary_paytime"),
        col("Company Name").alias("company_name"),
        col("Location").alias("location"),
        col("Start Date").alias("start_date"),
        col("Telephone").alias("telephone"),
        col("Email").alias("email"),
        col("Job Description").alias("job_description"),
        col("`Ref.-Nr.`").alias("ref_no"),
        col("External Link").alias("external_link"),
        col("Application Link").alias("application_link")
    )

    write_df_to_postgres(df, "german_web_data", "(profession,salary_min,salary_max,salary_unit,salary_paytime,company_name,location,start_date,telephone,email,job_description,ref_no,external_link,application_link)", "ref_no")



