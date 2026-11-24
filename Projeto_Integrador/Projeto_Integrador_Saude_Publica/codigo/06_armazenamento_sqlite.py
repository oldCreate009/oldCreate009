"""Etapa 3/7: exporta tabelas tratadas a SQLite, para inspeção local e SQL."""
from pathlib import Path
import sqlite3
import pandas as pd

def carregar(root:Path):
    db=root/'dados/projeto_saude.db'
    with sqlite3.connect(db) as c:
        for nome,path in {
            'fato_notificacoes':'dados/03_tratados/saude_bairro_semana_doenca.csv',
            'fato_vendas_farmacia':'dados/03_tratados/farmacia_vendas_tratadas.csv',
            'dash_serie_mensal':'dados/04_dashboard/01_serie_mensal_doencas.csv',
            'dash_bairros':'dados/04_dashboard/02_mapa_bairros.csv',
            'dash_previsoes':'dados/04_dashboard/06_previsoes_teste_temporal.csv',
            'dim_bairro':'dados/02_simulados/bairros.csv',
        }.items():
            df=pd.read_csv(root/path,encoding='utf-8-sig')
            df.to_sql(nome,c,if_exists='replace',index=False)
        c.execute('CREATE INDEX IF NOT EXISTS idx_epidemiologico ON fato_notificacoes (semana_inicio,bairro_id,doenca)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_farmacia ON fato_vendas_farmacia (data_venda,id_filial)')
    return db

if __name__=='__main__':
    print(carregar(Path(__file__).resolve().parents[1]))
