from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.transfers.gdrive_to_local import GoogleDriveToLocalOperator
from airflow.operators.bash import BashOperator


import psycopg2 as pg
import pandas as pd

import os
from sqlalchemy import create_engine,text
import gdown

from datetime import datetime,date


def get_csv(): #função para pegar o csv da pasta do drive
    data = date.today() #data atual
    output = f'/opt/airflow/extract/{data}' #para onde vai o arquivo
    url ='https://drive.google.com/drive/u/1/folders/1Fcc5jrON7faoLUPslby8kU4vJUZfyEVS' #endereço em que esta o arquivo
    gdown.download_folder(url,output=output) # informamos o endereço do drive e depois informamos para onde o arquivo vai

def csv_to_postgres():
    data = date.today() #data atual
    address = f'/opt/airflow/extract/{data}' #endereço em que esta nosso csv

    archives = os.listdir(address) #listamos os arquivos presentes na pasta

    conn = pg.connect(host='host.docker.internal', user='postgres', password='[coloque sua senha]', port=[informe sua porta], database='[informe o seu banco de dados]')# dados da conexão
  

    cursor = conn.cursor() # abrindo a conexão

    for archive in archives: #para cada arquivos que esta na nossa pasta
        match archive: #criamos uma tabela para o nosso arquivo
            case 'estados_dados.csv':
                cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {archive[:-4]} (
                    Estado character varying(255) NOT NULL,
                    sigla character varying(2) NOT NULL,
                    Região character varying(20) NOT NULL,
                    PIB_2022 double precision,
                    População_2022 bigint
                );
            """)
                
    for archive in archives: #aqui populamos a tabela
         with open(f'{address}/{archive}','r') as f:
                
            tableName = archive[:-4]

            next(f)
            cursor.copy_from(f,f'{tableName}',sep=';')

    conn.commit()

with DAG( # criando a dag
    dag_id='MiniProject',
    start_date=datetime(2023, 1, 1),
    schedule='35 7 * * *',
    catchup=False
) as dag: # aqui estão as tasks da dag
    start=EmptyOperator(task_id='start')
    criar_pasta = BashOperator(
    task_id='criar_pasta',
    bash_command=f'mkdir -p /opt/airflow/extract/{date.today()}',
    dag=dag,
)
    get_csv=PythonOperator(
        task_id='get_csv',
        python_callable=get_csv,
        op_kwargs={'today': '{{ds}}', 'param2': 'value2'} 
    )
    csv_to_postgres=PythonOperator(
        task_id='csv_to_postgres',
        python_callable=csv_to_postgres,
        op_kwargs={'today': '{{ds}}', 'param2': 'value2'} 
    )
start >>criar_pasta>>[get_csv] >> csv_to_postgres