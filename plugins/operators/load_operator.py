import logging
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadOperator(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 aws_credentials="",
                 insert_sql="",
                 *args,**kwargs):
        super(LoadOperator,self).__init__(*args,**kwargs)
        self.table=table
        self.redshift_conn_id=redshift_conn_id
        self.aws_credentials=aws_credentials
        self.insert_sql=insert_sql
        
    def execute(self, context):
        """
        Insert data into a table
        """
        redshift_hook=PostgresHook(postgres_conn_id=self.redshift_conn_id)
        redshift_hook.run(self.insert_sql)
        logging.info(f"Insert query : {self.insert_sql}")
        