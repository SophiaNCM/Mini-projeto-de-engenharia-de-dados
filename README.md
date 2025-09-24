# Conversão de dados
### Nesse projeto foi usado:
<ul><li>Python</li>
  <li>Docker</li>
  <li>Airflow</li>
</ul>

### Objetivo 
O objetivo desse codigo é importar um arquivo externo e colocar as informações que estão dentro dele em um database no postgres

### Caso queira testar
<ul><li>Baixe os arquivos, e coloque eles na mesma pasta</li>
  <li>Abra o docker desktop (não é possivel fazer o passo a passo sem ele)</li>
  <li>Abra no vs code ou onde preferir</li>
   <li>Vá no arquivo "dag_conversão.py" que está em dags, procure a função csv_to_postgres e informe seus dados na conexão (não mude o host, mas caso seu user seja diferente, mude ele também)</li>
  <li>Abra o terminal e digite:
    <blockquote>
    $ docker build . --tag extending_airflow:latest <!--esse comando serve para criar a imagem do airflow que é usada nesse projeto-->
    </br>
     $ docker compose up
    </blockquote>
    o docker build . --tag extending_airflow:latest -> serve para criar a imagem do airflow que é usada nesse projeto </br>
    docker compose up -> comando que cria nosso container
  
  </li>
  <li>Agora acesse: http://localhost:8080 </br>digite seu user e senha (provavelmente seu user é: airflow | sua senha é: airflow)</li>
  <li>Vá em DAGs e procure por MiniProject</li>
  <li>Agora é só rodar</li>
</ul>
