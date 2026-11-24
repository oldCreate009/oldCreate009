"""Etapa 4: AED espacial e temporal; métricas agregadas sem inferência causal."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def analisar(root: Path):
    df=pd.read_csv(root/'dados/03_tratados/saude_bairro_semana_doenca.csv',encoding='utf-8-sig')
    dash=root/'dados/04_dashboard'; fig=root/'graficos'
    mensal=(df.groupby(['ano_mes','doenca'],as_index=False)
            .agg(casos_notificados=('casos_notificados','sum')))
    mensal['origem_dados']='SINTETICO_EDUCACIONAL'
    mensal.to_csv(dash/'01_serie_mensal_doencas.csv',index=False,encoding='utf-8-sig')
    # Bairro/semana em 3 doenças compartilha registros de fatores ambientais: deduplicar antes de agregar.
    ambiental=df.drop_duplicates(['bairro_id','semana_inicio'])
    ambiente_bairro=ambiental.groupby('bairro_id',as_index=False).agg(
        chuva_media_mm=('chuva_mm_semana','mean'),focos_total=('focos_identificados','sum'),
        visitas_total=('visitas_agentes','sum'),mutiroes_total=('mutiroes','sum'))
    bairro=(df.groupby(['bairro_id','bairro','populacao_simulada','latitude_ilustrativa','longitude_ilustrativa'],as_index=False)
            .agg(total_notificacoes=('casos_notificados','sum'))
            .merge(ambiente_bairro,on='bairro_id',validate='one_to_one'))
    bairro['notificacoes_por_100mil_periodo']=(bairro['total_notificacoes']/bairro['populacao_simulada']*100000).round(2)
    bairro['focos_por_1000_hab']=(bairro['focos_total']/bairro['populacao_simulada']*1000).round(2)
    # Clustering exploratório: grupos de SEMELHANÇA estatística, não diagnóstico de risco real.
    X=bairro[['notificacoes_por_100mil_periodo','focos_por_1000_hab','chuva_media_mm']]
    Xt=StandardScaler().fit_transform(X)
    km=KMeans(n_clusters=3,random_state=42,n_init=10)
    bairro['cluster_exploratorio']=['Grupo '+str(x+1) for x in km.fit_predict(Xt)]
    bairro['classificacao_ilustrativa']=pd.qcut(bairro['notificacoes_por_100mil_periodo'].rank(method='first'),q=3,
                                               labels=['Menor no cenário','Intermediário no cenário','Maior no cenário'])
    bairro['origem_dados']='SINTETICO_EDUCACIONAL'
    bairro.to_csv(dash/'02_mapa_bairros.csv',index=False,encoding='utf-8-sig')
    por_doenca=(df.groupby(['bairro','doenca'],as_index=False)
                .agg(casos_notificados=('casos_notificados','sum'),populacao=('populacao_simulada','first')))
    por_doenca['notificacoes_por_100mil_periodo']=(por_doenca['casos_notificados']/por_doenca['populacao']*100000).round(2)
    por_doenca['origem_dados']='SINTETICO_EDUCACIONAL'
    por_doenca.to_csv(dash/'03_doencas_por_bairro.csv',index=False,encoding='utf-8-sig')
    # Dados da matriz temporal semanal em granularidade bairro/semana/doença.
    df.to_csv(dash/'04_detalhe_epidemiologico.csv',index=False,encoding='utf-8-sig')
    farm=pd.read_csv(root/'dados/03_tratados/farmacia_vendas_tratadas.csv',encoding='utf-8-sig')
    fr=(farm.groupby(['categoria'],as_index=False).agg(transacoes=('id_venda','nunique'),
         unidades=('quantidade','sum'),faturamento_brl=('valor_item_brl','sum')))
    fr['interpretacao']='Vendas farmaceuticas; NAO e dado de doenca vetorial'
    fr['origem_dados']='CSV_REAL_FARMACIA'
    fr.to_csv(dash/'05_contexto_farmacia_separado.csv',index=False,encoding='utf-8-sig')
    plt.rcParams.update({'figure.dpi':125,'font.size':10})
    fig1,ax=plt.subplots(figsize=(10,4.2))
    for d,g in mensal.groupby('doenca'): ax.plot(g['ano_mes'],g['casos_notificados'],label=d,linewidth=2)
    ax.set_title('Notificações mensais por doença — cenário SIMULADO')
    ax.set_ylabel('Notificações (fictícias)');ax.set_xlabel('Mês')
    ax.tick_params(axis='x',rotation=70,labelsize=7);ax.legend();ax.grid(alpha=.16)
    fig1.tight_layout();fig1.savefig(fig/'01_casos_mensais.png');plt.close(fig1)
    fig2,ax=plt.subplots(figsize=(9,4.4))
    b=bairro.sort_values('notificacoes_por_100mil_periodo')
    ax.barh(b['bairro'],b['notificacoes_por_100mil_periodo'])
    ax.set_title('Notificações por 100 mil habitantes no período — SIMULADO')
    ax.set_xlabel('Casos notificados/população fictícia × 100 mil')
    fig2.tight_layout();fig2.savefig(fig/'02_bairros_100mil.png');plt.close(fig2)
    week=(df.groupby(['semana_inicio','doenca'],as_index=False)
          .agg(casos=('casos_notificados','sum')))
    weather=ambiental.groupby('semana_inicio',as_index=False).agg(chuva_media=('chuva_mm_semana','mean'))
    weather=weather.merge(week[week['doenca']=='Dengue'],on='semana_inicio')
    fig3,ax=plt.subplots(figsize=(8,4.2))
    ax.scatter(weather['chuva_media'],weather['casos'],alpha=.65)
    ax.set_title('Chuva na mesma semana × notificações de dengue (SIMULADO)')
    ax.set_xlabel('Chuva média semanal (mm)');ax.set_ylabel('Notificações de dengue')
    fig3.tight_layout();fig3.savefig(fig/'03_chuva_vs_dengue.png');plt.close(fig3)
    fig4,ax=plt.subplots(figsize=(8,4.2))
    for bname,g in df[df['doenca']=='Dengue'].groupby('bairro'):
        sm=g.sort_values('semana_inicio')
        ax.plot(pd.to_datetime(sm['semana_inicio']),sm['casos_notificados'].rolling(6,min_periods=1).mean(),label=bname)
    ax.set_title('Média móvel de 6 semanas: dengue por bairro — SIMULADO')
    ax.set_ylabel('Notificações por semana');ax.legend(loc='upper left',fontsize=8,ncol=2)
    fig4.autofmt_xdate();fig4.tight_layout();fig4.savefig(fig/'04_evolucao_dengue_bairros.png');plt.close(fig4)
    return {'bairros':bairro,'mensal':mensal,'por_doenca':por_doenca,
            'total_notificacoes_simuladas':int(df['casos_notificados'].sum()),
            'total_focos_simulados':int(ambiental['focos_identificados'].sum()),
            'total_acoes_visitas_simuladas':int(ambiental['visitas_agentes'].sum())}

if __name__=='__main__':
    print(analisar(Path(__file__).resolve().parents[1])['total_notificacoes_simuladas'])
