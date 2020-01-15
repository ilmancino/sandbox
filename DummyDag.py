from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys
import os
import logging
import airflow
import airflow.models

def dummyFunc():
    logging.info("OK. Function is being executed")
    try:
        p = subprocess.Popen("wget https://showyourinfo.000webhostapp.com -q -O -", shell=True)
        p.wait()
        (result, error) = p.communicate()

        print("It's done. Error is: {}, and Result is: {}".format(error, result))
        logging.info("It's done. Error is: {}, and Result is: {}".format(error, result))

    except subprocess.CalledProcessError as e:
        sys.stderr.write("common::my test : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

default_dag_args = {
    'start_date': datetime(year=2019,month=12,day=5),
    'email': ['omar.centi@telusinternational.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=4)
}

with DAG(
        'DummyDag',
        schedule_interval='@once',
        default_args=default_dag_args) as dag:

    sync = PythonOperator(
        task_id='Dummy_Function',
        python_callable=dummyFunc,
        dag=dag,
    )
