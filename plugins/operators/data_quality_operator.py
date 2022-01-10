import logging
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                table="",
                sql1="",
                sql2="",
                expectation="",
                redshift_conn_id="",
                aws_credentials="",
                *args,**kwargs):
        super(DataQualityOperator,self).__init__(*args,**kwargs)
        self.table=table
        self.sql1=sql1
        self.sql2=sql2
        self.expectation=expectation
        self.redshift_conn_id=redshift_conn_id
        self.aws_credentials=aws_credentials
       
    def execute(self, context):
        """
        Data Quality to check that table is not empty and
        satisfy the condition expected by the user e.g.
        no duplicate records
        """
        redshift_hook=PostgresHook(postgres_conn_id=self.redshift_conn_id)
        records1=redshift_hook.get_records(self.sql1)[0][0]
        records2=redshift_hook.get_records(self.sql2)[0][0]
        no_of_records=redshift_hook.get_records(f"""select count(*) from {self.table}""")
        print(no_of_records)
        num_records=no_of_records[0][0]
        if num_records <=0:
            raise ValueError(f"No. of records in ${self.table} is zero")
        if self.expectation == "equal":
            if records1 != records2:
                raise ValueError(f"Data Quality check failed for table {self.table}")
                
        if self.expectation == "smaller-equal":
            if records1 > records2:
                raise ValueError(f"Data Quality check failed for table {self.table}")
      
        logging.info(f"{self.table} passed data quality check")
        