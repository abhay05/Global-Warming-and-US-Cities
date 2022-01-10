# Global-Warming-and-US-Cities
Udacity Capstone Project


## Purpose

To prepare data to anaylyse if there is any relation between population of an area and land temperature. For this is I will be using Global Land Temp data data and state_census of US big cities.

## Pipeline Architecture Diagram

![PipelineArchitecture](https://user-images.githubusercontent.com/23046900/147948965-bb76fc75-3f9d-404c-983f-1569f176bd7e.jpg)


## Data Model

![DataModel](https://user-images.githubusercontent.com/23046900/148059288-d2baf655-72b8-477d-9a51-dc705a7d228c.jpg)


## Exploring the Data

All the data is loaded into staging tables and cleaning is performed after that.
Global Temp Data -> There are some values with NA/NULL values, basically decided to drop the records where fields of interest had null values.
State Census -> There are some records with null,"(NA)" values , so these records are dropped after reading the csv.


## ETL Pipeline

1. Copy csv/json to s3.
2. Load data from s3 to staging table
3. Load dimension tables after fitlering,cleaning staging table.
4. Create fact table from dimension table
5. Put data quality checks after loading dimension and fact tables.
6. Since data includes census data and land temperature data, both of which need to be observed over a period
   of time to provide some valuable metric, data should be updated yearly


## Tech Stack used 

1. S3
2. Reshift
3. Airflow

S3 -> to store source data.
Reshift -> as a data warehouse.
Airflow -> For orchestraction of different steps in data pipeline

Reasons behind using this tech stack

S3 -> Security, Reliability, Availability and low cost.
Redshift -> It's scalable, supports columnar storage and provides MPP(Massively parallel processing)
Airflow -> It's user friendly, easy to use and highly customizable.


## Scenarios

**If the data was increased by 100x.**
> I would modify this architecture, use emr clusters with spark to perform etl steps along with S3 to store
input and ouptut, spark is really fast and useful in handling big data. Spark can leverage availability of 
multiple nodes in a cluster and provide quick results.

**If the pipelines were run on a daily basis by 7am.**
> Update the airflow configuration according to the required scheduling, current architecture can support that.

**If the database needed to be accessed by 100+ people.**
> Make sure that security rules allow only read operations.
> Increase the cluster size if number of queries can't be handled with current settings.
