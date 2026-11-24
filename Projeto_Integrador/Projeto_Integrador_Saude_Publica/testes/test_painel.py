"""Conferência básica dos valores usados pelo dashboard HTML."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def ler(nome):
    return pd.read_csv(ROOT / 'dados/04_dashboard' / nome, encoding='utf-8-sig')


def test_dados_do_painel_sem_duplicar_focos():
    detalhe = ler('04_detalhe_epidemiologico.csv')
    mapa = ler('02_mapa_bairros.csv')
    ambiente = detalhe.drop_duplicates(['bairro_id', 'semana_inicio'])
    assert len(ambiente) == 6 * 104
    assert int(ambiente['focos_identificados'].sum()) == int(mapa['focos_total'].sum())


def test_dashboard_html_e_script_existem():
    html = (ROOT / 'docs/index.html').read_text(encoding='utf-8')
    dados = (ROOT / 'docs/assets/dados-painel.js').read_text(encoding='utf-8')
    assert 'DADOS_PAINEL' in dados and 'DADOS FICTÍCIOS' in dados
    assert all(p in html for p in ('data-aba="geral"', 'data-aba="bairros"', 'data-aba="modelo"'))
