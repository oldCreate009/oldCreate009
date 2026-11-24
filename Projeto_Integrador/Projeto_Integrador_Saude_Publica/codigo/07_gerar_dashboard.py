"""Etapa 7: prepara dados do painel HTML simples (GitHub Pages).

A fonte é sempre o CSV já tratado. A tabela de focos não é somada por doença:
ela é deduplicada por bairro e semana antes da agregação mensal.
"""
from pathlib import Path
import json
import pandas as pd


def gerar(raiz: Path):
    raiz = Path(raiz)
    origem = raiz / 'dados' / '04_dashboard'
    tabela = pd.read_csv(origem / '04_detalhe_epidemiologico.csv', encoding='utf-8-sig')
    bairros = pd.read_csv(origem / '02_mapa_bairros.csv', encoding='utf-8-sig')
    previsoes = pd.read_csv(origem / '06_previsoes_teste_temporal.csv', encoding='utf-8-sig')

    if not (tabela['origem_dados'] == 'SINTETICO_EDUCACIONAL').all():
        raise ValueError('Origem epidemiológica inesperada')
    if not (previsoes['origem_dados'] == 'SINTETICO_EDUCACIONAL').all():
        raise ValueError('Previsões sem marcador de simulação')
    if tabela.duplicated(['bairro_id', 'semana_inicio', 'doenca']).any():
        raise ValueError('Há registros epidemiológicos duplicados')

    # Casos: agregação mês / bairro / doença.
    casos = (tabela.groupby(['ano_mes', 'bairro_id', 'doenca'], as_index=False)
             ['casos_notificados'].sum()
             .rename(columns={'ano_mes': 'mes', 'bairro_id': 'bairro',
                              'casos_notificados': 'total'})
             .sort_values(['mes', 'bairro', 'doenca']))

    # Chuva, focos e visitas se repetem nas 3 doenças. Deduplicar primeiro.
    ambiente = tabela.drop_duplicates(['semana_inicio', 'bairro_id'])
    controle = (ambiente.groupby(['ano_mes', 'bairro_id'], as_index=False)
                [['focos_identificados', 'visitas_agentes', 'focos_eliminados', 'mutiroes']]
                .sum()
                .rename(columns={'ano_mes': 'mes', 'bairro_id': 'bairro',
                                 'focos_identificados': 'focos',
                                 'visitas_agentes': 'visitas',
                                 'focos_eliminados': 'eliminados'})
                .sort_values(['mes', 'bairro']))

    # Manter somente o teste temporal para comunicar previsão, não prometer futuro.
    previsoes = (previsoes[['semana_inicio', 'bairro_id', 'doenca',
                             'casos_notificados', 'previsto_modelo',
                             'previsto_baseline_lag1']]
                 .rename(columns={'semana_inicio': 'semana', 'bairro_id': 'bairro',
                                  'casos_notificados': 'real',
                                  'previsto_modelo': 'previsto',
                                  'previsto_baseline_lag1': 'base'})
                 .sort_values(['semana', 'bairro', 'doenca']))

    territorios = (bairros[['bairro_id', 'bairro', 'populacao_simulada',
                            'latitude_ilustrativa', 'longitude_ilustrativa']]
                   .rename(columns={'bairro_id': 'id', 'bairro': 'nome',
                                    'populacao_simulada': 'populacao',
                                    'latitude_ilustrativa': 'lat',
                                    'longitude_ilustrativa': 'lon'})
                   .sort_values('id'))

    dados = {
        'aviso': 'DADOS FICTÍCIOS PARA FINS DIDÁTICOS. Não são dados de vigilância real.',
        'bairros': territorios.to_dict(orient='records'),
        'casos': casos.to_dict(orient='records'),
        'controle': controle.to_dict(orient='records'),
        'previsoes': previsoes.to_dict(orient='records'),
    }
    saida = raiz / 'docs' / 'assets' / 'dados-painel.js'
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text('/* Gerado pelo script codigo/07_gerar_dashboard.py. */\n'
                     'window.DADOS_PAINEL = '
                     + json.dumps(dados, ensure_ascii=False, indent=1, allow_nan=False)
                     + ';\n', encoding='utf-8')
    return {'registros_casos_agrupados': len(casos),
            'registros_controle_agrupados': len(controle),
            'registros_previsoes': len(previsoes),
            'arquivo': str(saida.relative_to(raiz))}


if __name__ == '__main__':
    print(gerar(Path(__file__).resolve().parents[1]))
