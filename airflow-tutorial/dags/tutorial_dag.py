from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import requests
import json

def captura_conta_dados():
    url = "https://data.cityofnetwork.us/resource/rc75-m7u3.json"
    response = requests.get(url)
    df = pd.DataFrame(json.loads(response.content))
    qtd = len(df.index)
    return qtd

def e_valido(ti):
    qtd = ti.xcom_pull(tasks_id = 'captura_conta_dados')
    if qtd > 1000:
        return 'valido'
    return 'não valido'

with DAG('tutorial_dag', start_date = datetime(2021, 12, 1),
         schedule_interval = '30 * * * *', catchup=False) as dag:
    
    captura_conta_dados = PythonOperator(
        task_id = 'captura_dados_dados',
        python_callable = captura_conta_dados
    )
    e_valido = BranchPythonOperator(
        task_id = 'e_valida',
        python_callable = e_valido
    )

    valido = BashOperator(
        task_id = 'valido',
        bash_command = "echo 'Quantidade OK'"
    )

    nvalido = BashOperator(
        task_id = 'nvalido',
        bash_command = "echo 'Quantidade não OK'"
    )

    captura_conta_dados >> e_valido >> [valido, nvalido]