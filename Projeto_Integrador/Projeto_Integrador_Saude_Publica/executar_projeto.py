"""Executa ETL, análise, modelo e atualiza dashboard HTML. Python 3.10+."""
from pathlib import Path
import importlib.util, json

RAIZ=Path(__file__).resolve().parent

def carregar_modulo(numero,nome):
    p=RAIZ/'codigo'/f'{numero}_{nome}.py'
    spec=importlib.util.spec_from_file_location(nome,p)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def executar():
    farmacia,audit=carregar_modulo('01','auditoria_farmacia').processar(RAIZ)
    origem=carregar_modulo('02','gerar_cenario_simulado').gerar(RAIZ)
    base=carregar_modulo('03','etl_epidemiologico').transformar(RAIZ)
    aed=carregar_modulo('04','analise_exploratoria').analisar(RAIZ)
    aval=carregar_modulo('05','modelagem_avaliacao').modelar(RAIZ)
    banco=carregar_modulo('06','armazenamento_sqlite').carregar(RAIZ)
    painel=carregar_modulo('07','gerar_dashboard').gerar(RAIZ)
    totais=base.groupby('doenca')['casos_notificados'].sum().astype(int).to_dict()
    mapa=aed['bairros'].sort_values('notificacoes_por_100mil_periodo',ascending=False)
    resumo={'tipo':'DADOS SINTÉTICOS PARA SAÚDE + CSV REAL DE FARMÁCIA SEPARADO',
            'farmacia':{'linhas':audit['linhas_brutas'],'faturamento_brl':audit['valor_total_brl'],
                       'filiais':audit['numero_filiais'],'sem_id_cliente':True},
            'cenario_sintetico':origem,'casos_sinteticos_total':aed['total_notificacoes_simuladas'],
            'casos_sinteticos_por_doenca':totais,
            'focos_sinteticos_total':aed['total_focos_simulados'],
            'visitas_sinteticas_total':aed['total_acoes_visitas_simuladas'],
            'bairro_maior_notificacoes_100mil':str(mapa.iloc[0]['bairro']),
            'bairro_maior_notificacoes_100mil_taxa':float(mapa.iloc[0]['notificacoes_por_100mil_periodo']),
            'modelo':aval,'banco_sqlite_gerado':str(banco.relative_to(RAIZ)),
            'dashboard_html':painel,
            'dashboard_status':'HTML interativo pronto; Google Looker Studio pendente'}
    (RAIZ/'relatorios/resumo_execucao.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(resumo,indent=2,ensure_ascii=False))
    return resumo

if __name__=='__main__': executar()
