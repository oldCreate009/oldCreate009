"""Etapa 2: cenário didático 100% fictício de vigilância de arboviroses.
 NÃO representa pacientes, notificações ou geolocalização reais. Reprodutível (seed=42).
"""
from pathlib import Path
import numpy as np
import pandas as pd

BAIRROS=[
 ('B01','Bairro Aurora',19000,-25.430,-49.315,1.10),
 ('B02','Bairro Esperança',35000,-25.438,-49.285,0.95),
 ('B03','Bairro Primavera',28000,-25.460,-49.307,1.40),
 ('B04','Bairro União',41000,-25.468,-49.274,0.80),
 ('B05','Bairro Horizonte',23500,-25.488,-49.320,1.55),
 ('B06','Bairro do Sol',32000,-25.490,-49.280,1.00),
]
DOENCAS=['Dengue','Chikungunya','Zika']

def gerar(root: Path,seed=42):
    rng=np.random.default_rng(seed)
    dest=root/'dados/02_simulados'
    semanas=pd.date_range('2024-01-01',periods=104,freq='7D')
    bairros=[];clima=[];focos=[];acoes=[];casos=[]
    for bid,nome,pop,lat,lon,risco in BAIRROS:
        bairros.append({'bairro_id':bid,'bairro':nome,'populacao_simulada':pop,
                        'latitude_ilustrativa':lat,'longitude_ilustrativa':lon,
                        'origem_dados':'SINTETICO_EDUCACIONAL'})
        historico={d:0 for d in DOENCAS}
        chuva_h=[];focos_h=[];acoes_h=[]
        for t,semana in enumerate(semanas):
            # Série temporal sazonal sintética, com dinâmica simplificada (não real).
            saz=max(-0.35,np.sin(2*np.pi*(t%52)/52 + 0.35))
            precipitacao=round(max(0.,rng.gamma(shape=2.2,scale=18)+32*saz+8*(risco-1)),1)
            temperatura=round(23+3*np.sin(2*np.pi*(t%52)/52 + 0.8)+rng.normal(0,1.2),1)
            nfocos=int(rng.poisson(max(0.8,4 + 0.075*precipitacao + 4*(risco-1))))
            visitas=int(rng.poisson(max(0.8,14+0.65*nfocos)))
            mutiroes=int(rng.binomial(2,0.25))
            eliminados=int(min(nfocos,rng.binomial(nfocos,0.35+0.09*mutiroes)))
            chuva_h.append(precipitacao);focos_h.append(nfocos);acoes_h.append(visitas)
            chave={'semana_inicio':semana.strftime('%Y-%m-%d'),'bairro_id':bid}
            clima.append({**chave,'chuva_mm_semana':precipitacao,'temp_media_c':temperatura,'origem_dados':'SINTETICO_EDUCACIONAL'})
            focos.append({**chave,'focos_identificados':nfocos,'origem_dados':'SINTETICO_EDUCACIONAL'})
            acoes.append({**chave,'visitas_agentes':visitas,'mutiroes':mutiroes,
                         'focos_eliminados':eliminados,'origem_dados':'SINTETICO_EDUCACIONAL'})
            for doenca in DOENCAS:
                multiplicador={'Dengue':1,'Chikungunya':0.28,'Zika':0.15}[doenca]
                chuva_lag=chuva_h[-3] if len(chuva_h)>2 else 35
                focos_lag=focos_h[-2] if len(focos_h)>1 else 5
                visitas_lag=acoes_h[-3] if len(acoes_h)>2 else 15
                # Efeito fictício de fatores defasados; não implica causalidade na vida real.
                esperado=(1.5 + 0.026*chuva_lag +0.35*focos_lag +0.12*historico[doenca]
                          -0.010*visitas_lag) * (pop/23000) * risco * multiplicador
                esperado=max(0.08,esperado)
                n=int(rng.poisson(esperado))
                casos.append({**chave,'doenca':doenca,'casos_notificados':n,
                              'origem_dados':'SINTETICO_EDUCACIONAL'})
                historico[doenca]=n
    for nome,dados in [('bairros.csv',bairros),('clima_semanal.csv',clima),('focos_semanal.csv',focos),
                       ('acoes_controle_semanal.csv',acoes),('casos_notificados_semanais.csv',casos)]:
        pd.DataFrame(dados).to_csv(dest/nome,index=False,encoding='utf-8-sig')
    return {'semanas':len(semanas),'bairros':len(BAIRROS),'doencas':len(DOENCAS),
            'notificacoes_linhas':len(casos),'nota':'Tudo sintético; cidades/coordenadas/indivíduos não são reais.'}

if __name__=='__main__':
    print(gerar(Path(__file__).resolve().parents[1]))
