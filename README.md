# Pipeline de Dados com PySpark

## Contexto

Uma empresa recebe arquivos de pedidos diariamente. O objetivo é transformar os arquivos brutos em uma camada analítica em Parquet, organizada por data.

## Arquitetura

```text
CSV / Bronze
    |
    v
PySpark
    |
    +--> limpeza
    +--> tipagem
    +--> remoção de duplicidades
    +--> regras de negócio
    |
    v
Parquet / Silver
    |
    v
Agregação / Gold
```

## Como executar

Requisitos:

- Python 3.10+
- Java compatível com a versão do Spark

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/pipeline.py
```

Saída:

```text
data/
├── raw/
├── silver/
└── gold/
```

## Transformações

A camada Silver:

- normaliza tipos;
- converte datas;
- remove registros inválidos;
- remove duplicidades;
- filtra pedidos pagos;
- calcula receita;
- particiona por ano/mês.

A camada Gold gera uma visão mensal por categoria.

## Decisões técnicas

O projeto utiliza Parquet porque o formato é colunar e adequado para workloads analíticos. A Silver é particionada por ano/mês para permitir leitura seletiva.

## Competências

`PySpark` `Spark SQL` `ETL` `Parquet` `Data Lake` `Partitioning` `Data Quality`
