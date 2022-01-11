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


## Data Dictionary

| Field Name | Data Type | Field Size for display | Description | Table Name |
| ---------- | --------- | ---------------------- | ----------- | ---------- |
| dt | Date |  | Date of a particular record | dim_land_temp , dim_time |
| city | varchar | 30 | Name of a city | dim_land_temp , dim_city, dim_city_pop, fact_city_temp_n_pop |
| averageTemperature | float | 15 | Average land temperature of a city on a day | dim_land_temp , fact_city_temp_n_pop |
| averageTemperatureUncertainty | float | 15 | uncertainty in average temperature for a day  | dim_land_temp , fact_city_temp_n_pop |
| year | int | 4 | Year  | dim_city_pop, dim_time , fact_city_temp_n_pop |
| state | varchar | 30 | A US state  | dim_city_pop , fact_city_temp_n_pop |
| population | int |  | Population of a city  | dim_city_pop , fact_city_temp_n_pop |
| country | varchar | 30 | Country name  | dim_city , fact_city_temp_n_pop |
| latitude | varchar | 10 | latitude | dim_city , fact_city_temp_n_pop |
| longitude | varchar | 10 | longitude  | dim_city , fact_city_temp_n_pop |
| month | int | 2 | Month  | dim_time |
| day | int | 2 | Day  | dim_time |
| id | varchar | 50 | unique md5 id  | fact_city_temp_n_pop |


## Airflow Run

![Capstone-Graph-View](https://user-images.githubusercontent.com/23046900/148825809-d0edb1d0-5dc8-48b9-8478-8dbb0af2c5a7.PNG)

![Capstone-Tree-View](https://user-images.githubusercontent.com/23046900/148825842-92bfa4ea-ea39-493f-8761-5693cc3b246a.PNG)


## Final Data Output Sample

> select * from fact_city_temp_n_pop limit 10;

![Capstone-final-table-output](https://user-images.githubusercontent.com/23046900/148954004-d1fbbdae-5bb5-493e-b393-2bcab89001ee.PNG)


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
