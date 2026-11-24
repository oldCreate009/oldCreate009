from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def csv(path):return pd.read_csv(ROOT/path,encoding='utf-8-sig')

def test_casos_tem_granularidade_unica():
    c=csv('dados/03_tratados/saude_bairro_semana_doenca.csv')
    assert len(c)==6*104*3
    assert not c.duplicated(['bairro_id','semana_inicio','doenca']).any()
    assert (c['casos_notificados']>=0).all()
    assert set(c['doenca'])=={'Dengue','Zika','Chikungunya'}
    assert (c['origem_dados']=='SINTETICO_EDUCACIONAL').all()

def test_publico_sem_cliente():
    p=csv('dados/01_publico/farmacia_sem_id_cliente.csv')
    t=csv('dados/03_tratados/farmacia_vendas_tratadas.csv')
    assert len(p)==50 and len(t)==50
    assert 'ID_Cliente' not in p.columns
    assert 'id_cliente' not in t.columns
    assert (t['origem_dados']=='farmacia_vendas_csv_usuario').all()
    assert not t['divergencia_financeira'].any()

def test_sem_duplicacao_de_clima_e_focos():
    c=csv('dados/03_tratados/saude_bairro_semana_doenca.csv')
    ambiente=c.drop_duplicates(['bairro_id','semana_inicio'])
    assert len(ambiente)==6*104
    assert ambiente['focos_identificados'].sum()==csv('dados/02_simulados/focos_semanal.csv')['focos_identificados'].sum()

def test_sem_vazamento_temporal_obvio():
    c=csv('dados/03_tratados/saude_bairro_semana_doenca.csv')
    for (_, _),g in c.groupby(['bairro_id','doenca']):
        g=g.sort_values('semana_inicio')
        assert g['casos_lag1'].iloc[1:].reset_index(drop=True).equals(g['casos_notificados'].shift(1).iloc[1:].reset_index(drop=True).astype('float64'))

def test_previsoes_somente_simuladas():
    p=csv('dados/04_dashboard/06_previsoes_teste_temporal.csv')
    assert not p.empty
    assert (p['semana_inicio']>='2025-07-07').all()
    assert (p['origem_dados']=='SINTETICO_EDUCACIONAL').all()
