# Remember to run "/opt/airflow/start.sh" command to start the web server. Once the Airflow web server is ready,  open the Airflow UI using the "Access Airflow" button. Turn your DAG “On”, and then Run your DAG. If you get stuck, you can take a look at the solution file in the workspace/airflow/dags folder in the workspace and the video walkthrough on the next page.

import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators import (
    HasRowsOperator,
    S3ToRedshiftOperator,
    LoadOperator,
    DataQualityOperator
)

from helpers import (
    SqlQueries
)

#Airflow dag to orchestrate etl

dag = DAG("capstone-practice", start_date=datetime.datetime.utcnow())


start_operator=DummyOperator(task_id="begin_execution",dag=dag)

copy_pop_task = S3ToRedshiftOperator(
    task_id="load_city_population_from_s3_to_redshift",
    dag=dag,
    table="staging_city_population",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstone-source-asc",
    s3_key="state_census.csv"    
)

copy_temp_task = S3ToRedshiftOperator(
    task_id="load_global_land_temp_from_s3_to_redshift",
    dag=dag,
    table="staging_global_land_temp",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstone-source-asc",
    s3_key="GlobalLandTemperaturesByCity.csv"    
)

load_dim_city_pop = LoadOperator(
    task_id="load_dim_city_pop_table",
    dag=dag,
    table="dim_city_pop",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials",
    insert_sql=SqlQueries.InsertIntoDimCityPop
)

load_dim_land_temp = LoadOperator(
    task_id="load_dim_land_temp_table",
    dag=dag,
    table="dim_land_temp",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials",
    insert_sql=SqlQueries.InsertIntoDimLandTemp
)

load_dim_city = LoadOperator(
    task_id="load_dim_city_table",
    dag=dag,
    table="dim_city",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials",
    insert_sql=SqlQueries.InsertIntoDimCity
)

load_dim_time = LoadOperator(
    task_id="load_dim_time_table",
    dag=dag,
    table="dim_time",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials",
    insert_sql=SqlQueries.InsertIntoDimTime
)

load_fact_city_temp_n_pop = LoadOperator(
    task_id="load_fact_city_temp_n_pop_table",
    dag=dag,
    table="fact_city_temp_n_pop",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials",
    insert_sql=SqlQueries.InsertIntoFactCityTempNPop
)

data_quality_check_dim_city_pop = DataQualityOperator(
    task_id="check_data_quality_dim_city_pop",
    dag=dag,
    table="dim_city_pop",
    sql1="select count(*) from dim_city_pop",
    sql2="select count(*) from (select city from dim_city_pop group by year,city)",
    expectation="equal",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials"
    
)

data_quality_check_dim_land_temp = DataQualityOperator(
    task_id="check_data_quality_dim_land_temp",
    dag=dag,
    table="dim_land_temp",
    sql1="select count(*) from dim_land_temp",
    sql2="select count(*) from (select city from dim_land_temp group by dt,city)",
    expectation="equal",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials"
    
)

data_quality_check_dim_city = DataQualityOperator(
    task_id="check_data_quality_dim_city",
    dag=dag,
    table="dim_city",
    sql1="select count(*) from dim_city",
    sql2="select count(distinct(city)) from dim_city",
    expectation="equal",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials"
    
)

data_quality_check_dim_time = DataQualityOperator(
    task_id="check_data_quality_dim_time",
    dag=dag,
    table="dim_time",
    sql1="select count(*) from dim_time",
    sql2="select count(distinct(dt)) from dim_time",
    expectation="equal",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials"
    
)

data_quality_check_fact_city_temp_n_pop = DataQualityOperator(
    task_id="check_data_quality_fact_city_temp_n_pop",
    dag=dag,
    table="fact_city_temp_n_pop",
    sql1="select count(*) from fact_city_temp_n_pop",
    sql2="select count(*) from dim_city_pop",
    expectation="smaller-equal",
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials"
    
)

end_operator=DummyOperator(task_id="end_execution",dag=dag)

start_operator>>copy_pop_task
start_operator>>copy_temp_task
copy_pop_task>>load_dim_city_pop
copy_temp_task>>load_dim_land_temp
copy_temp_task>>load_dim_city
copy_temp_task>>load_dim_time
load_dim_city_pop>>data_quality_check_dim_city_pop
load_dim_land_temp>>data_quality_check_dim_land_temp
load_dim_city>>data_quality_check_dim_city
load_dim_time>>data_quality_check_dim_time
data_quality_check_dim_city_pop>>load_fact_city_temp_n_pop
data_quality_check_dim_land_temp>>load_fact_city_temp_n_pop
data_quality_check_dim_city>>load_fact_city_temp_n_pop
data_quality_check_dim_time>>load_fact_city_temp_n_pop
load_fact_city_temp_n_pop>>data_quality_check_fact_city_temp_n_pop
data_quality_check_fact_city_temp_n_pop>>end_operator
