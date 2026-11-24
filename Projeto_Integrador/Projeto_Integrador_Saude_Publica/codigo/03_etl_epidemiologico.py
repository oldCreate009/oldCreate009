"""Etapa 3: ETL de notificações e contexto ambiental em granularidade bairro-semana-doença."""
from pathlib import Path
import pandas as pd
import numpy as np

def transformar(root:Path):
    inp=root/'dados/02_simulados'; out=root/'dados/03_tratados'
    load=lambda n: pd.read_csv(inp/n,encoding='utf-8-sig')
    dados=load('casos_notificados_semanais.csv')
    clima=load('clima_semanal.csv')
    focos=load('focos_semanal.csv')
    acoes=load('acoes_controle_semanal.csv')
    bairros=load('bairros.csv')
    chaves=['semana_inicio','bairro_id']
    if dados.duplicated(chaves+['doenca']).any(): raise ValueError('Notificações duplicadas por bairro/semana/doença')
    for nome,df in [('clima',clima),('focos',focos),('acoes',acoes)]:
        if df.duplicated(chaves).any(): raise ValueError(f'{nome}: chaves duplicadas')
    if bairros['bairro_id'].duplicated().any(): raise ValueError('Bairro duplicado')
    for c in ['casos_notificados']:
        if dados[c].isna().any() or (dados[c]<0).any(): raise ValueError('Caso inválido')
    df=(dados.merge(clima.drop(columns='origem_dados'),on=chaves,how='left',validate='many_to_one')
         .merge(focos.drop(columns='origem_dados'),on=chaves,how='left',validate='many_to_one')
         .merge(acoes.drop(columns='origem_dados'),on=chaves,how='left',validate='many_to_one')
         .merge(bairros.drop(columns='origem_dados'),on='bairro_id',how='left',validate='many_to_one'))
    essenciais=['chuva_mm_semana','focos_identificados','visitas_agentes','populacao_simulada']
    if df[essenciais].isna().any().any(): raise ValueError('Falha de integridade: dados ambientais ou população ausentes')
    df['semana_inicio']=pd.to_datetime(df['semana_inicio'],errors='raise')
    df=df.sort_values(['bairro_id','doenca','semana_inicio']).reset_index(drop=True)
    df['ano']=df['semana_inicio'].dt.year
    df['mes']=df['semana_inicio'].dt.month
    df['ano_mes']=df['semana_inicio'].dt.strftime('%Y-%m')
    df['semana_iso']=df['semana_inicio'].dt.isocalendar().week.astype(int)
    df['incidencia_100mil_semana']=((df['casos_notificados']/df['populacao_simulada'])*100000).round(4)
    grupo=df.groupby(['bairro_id','doenca'],sort=False)
    df['casos_lag1']=grupo['casos_notificados'].shift(1)
    df['casos_lag2']=grupo['casos_notificados'].shift(2)
    df['casos_lag4']=grupo['casos_notificados'].shift(4)
    df['media_movel_4s']=grupo['casos_notificados'].transform(lambda x:x.shift(1).rolling(4).mean())
    # Fatores ambientais iguais em todas as doenças daquele bairro/semana; lag por doença é equivalente.
    for col,lag,name in [('chuva_mm_semana',2,'chuva_lag2'),('focos_identificados',1,'focos_lag1'),
                         ('visitas_agentes',2,'visitas_lag2'),('temp_media_c',1,'temp_lag1')]:
        df[name]=grupo[col].shift(lag)
    df['semana_inicio']=df['semana_inicio'].dt.strftime('%Y-%m-%d')
    df['tipo_dados']='SIMULADO_FICTICIO'
    df.to_csv(out/'saude_bairro_semana_doenca.csv',index=False,encoding='utf-8-sig')
    return df

if __name__=='__main__':
    print(transformar(Path(__file__).resolve().parents[1]).shape)
