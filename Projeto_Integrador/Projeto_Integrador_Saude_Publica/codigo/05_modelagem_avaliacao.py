"""Etapas 5-6: modelo descritivo/preditivo de 1 semana à frente com teste temporal.
Estritamente experimental em dados simulados. NÃO recomenda ações de saúde reais.
"""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CATEGORICAS=['bairro_id','doenca']
NUMERICAS=['populacao_simulada','casos_lag1','casos_lag2','casos_lag4',
           'media_movel_4s','chuva_lag2','focos_lag1','visitas_lag2','temp_lag1','mes']
FEATURES=CATEGORICAS+NUMERICAS
CUT_OFF='2025-07-07'

def modelar(root:Path):
    inp=root/'dados/03_tratados/saude_bairro_semana_doenca.csv'
    df=pd.read_csv(inp,encoding='utf-8-sig')
    df=df.dropna(subset=FEATURES+['casos_notificados']).copy()
    df=df.sort_values(['semana_inicio','bairro_id','doenca'])
    train=df[df['semana_inicio']<CUT_OFF].copy()
    teste=df[df['semana_inicio']>=CUT_OFF].copy()
    if len(train)<100 or len(teste)<50: raise ValueError('Séries insuficientes para divisão temporal')
    pp=ColumnTransformer([('categorias',OneHotEncoder(handle_unknown='ignore'),CATEGORICAS),
                          ('numericas','passthrough',NUMERICAS)])
    rf=RandomForestRegressor(n_estimators=160,min_samples_leaf=4,max_features=0.9,
                             random_state=42,n_jobs=1)
    modelo=Pipeline([('preparacao',pp),('regressor',rf)])
    modelo.fit(train[FEATURES],train['casos_notificados'])
    pred=np.maximum(0,modelo.predict(teste[FEATURES]))
    esperado=teste['casos_notificados'].to_numpy()
    base=teste['casos_lag1'].to_numpy()
    mae=float(mean_absolute_error(esperado,pred))
    rmse=float(np.sqrt(mean_squared_error(esperado,pred)))
    baseline_mae=float(mean_absolute_error(esperado,base))
    baseline_rmse=float(np.sqrt(mean_squared_error(esperado,base)))
    wape=float(abs(esperado-pred).sum()/max(1.0,abs(esperado).sum())*100)
    teste['previsto_modelo']=np.round(pred,2)
    teste['previsto_baseline_lag1']=base
    teste['erro_absoluto_modelo']=np.abs(teste['casos_notificados']-teste['previsto_modelo']).round(2)
    teste['origem_dados']='SINTETICO_EDUCACIONAL'
    teste[['semana_inicio','bairro_id','bairro','doenca','casos_notificados','previsto_modelo',
           'previsto_baseline_lag1','erro_absoluto_modelo','origem_dados']].to_csv(
           root/'dados/04_dashboard/06_previsoes_teste_temporal.csv',index=False,encoding='utf-8-sig')
    met={'projeto':'SIMULADO; NÃO USAR EM VIGILÂNCIA REAL','tipo_modelo':'RandomForestRegressor',
         'objetivo':'predizer notificações semanais por bairro e doença, a partir de informações passadas',
         'separacao_temporal_corte':CUT_OFF,'observacoes_treino':len(train),
         'observacoes_teste':len(teste),'mae_modelo':round(mae,4),
         'rmse_modelo':round(rmse,4),'wape_modelo_pct':round(wape,2),
         'mae_baseline_lag1':round(baseline_mae,4),'rmse_baseline_lag1':round(baseline_rmse,4),
         'modelo_supera_baseline_mae':bool(mae<baseline_mae),
         'features_estritamente_defasadas':['casos_lag1','casos_lag2','casos_lag4',
         'media_movel_4s','chuva_lag2','focos_lag1','visitas_lag2','temp_lag1'],
         'limite':'Dataset fictício; métricas NÃO validam desempenho em municípios reais.'}
    (root/'modelos/avaliacao_modelo.json').write_text(json.dumps(met,ensure_ascii=False,indent=2),encoding='utf-8')
    joblib.dump(modelo,root/'modelos/modelo_didatico.joblib')
    return met

if __name__=='__main__':
    print(modelar(Path(__file__).resolve().parents[1]))
