"""Etapa 2-3: audita e prepara, sem ampliar conclusões, o CSV real de farmácia."""
from pathlib import Path
import argparse, json
import pandas as pd

SOURCE = 'farmacia_vendas_csv_usuario'
COLS = {'ID_Venda':'id_venda','Data_Venda':'data_venda','Hora_Venda':'hora_venda',
 'ID_Filial':'id_filial','Nome_Filial':'nome_filial','ID_Produto':'id_produto',
 'Nome_Produto':'nome_produto','Categoria_Produto':'categoria',
 'Quantidade_Vendida':'quantidade','Preco_Unitario_R$':'preco_unitario_brl',
 'Valor_Total_Item_R$':'valor_item_brl','Tipo_Pagamento':'tipo_pagamento',
 'Produto_Promocao':'em_promocao'}

def processar(root: Path, verbose=True):
    privado=root/'dados/00_original_privado/Varejo_problema_1_ORIGINAL.csv'
    publico=root/'dados/01_publico/farmacia_sem_id_cliente.csv'
    tratado=root/'dados/03_tratados/farmacia_vendas_tratadas.csv'
    out=root/'relatorios/auditoria_dados_farmacia.json'
    if privado.exists():
        # Coluna ID_Cliente não será copiada aos arquivos publicáveis.
        bruto=pd.read_csv(privado,encoding='cp1252',dtype={'ID_Cliente':'string'})
        origem='csv_original_local'
    else:
        bruto=pd.read_csv(publico,encoding='utf-8-sig')
        origem='copia_publica_sem_id_cliente'
    faltantes=bruto.isna().sum().to_dict()
    erros=[]
    for c in ['ID_Venda','Data_Venda','ID_Filial','ID_Produto','Quantidade_Vendida','Preco_Unitario_R$','Valor_Total_Item_R$']:
        if c not in bruto.columns: erros.append(f'Coluna obrigatória ausente: {c}')
    if erros: raise ValueError('; '.join(erros))
    duplicatas_linhas=int(bruto.duplicated().sum())
    duplicatas_id=int(bruto.duplicated(subset=['ID_Venda']).sum())
    valores_divergentes=int(((bruto['Quantidade_Vendida']*bruto['Preco_Unitario_R$']-bruto['Valor_Total_Item_R$']).abs()>0.011).sum())
    invalido=int(((bruto['Quantidade_Vendida']<=0) | (bruto['Preco_Unitario_R$']<0)).sum())
    datas_invalidas=int(pd.to_datetime(bruto['Data_Venda'],errors='coerce').isna().sum())
    # Exporta cópia fiel nos campos não identificadores, usando UTF-8.
    bruto.drop(columns=['ID_Cliente'],errors='ignore').to_csv(publico,index=False,encoding='utf-8-sig')
    df=bruto.drop(columns=['ID_Cliente'],errors='ignore').rename(columns=COLS).copy()
    df['data_venda']=pd.to_datetime(df['data_venda'],errors='coerce').dt.strftime('%Y-%m-%d')
    df['ano_mes']=df['data_venda'].str.slice(0,7)
    df['origem_dados']=SOURCE
    df['finalidade']='analise_contextual_farmacia_nao_epi'
    df=df.drop_duplicates(subset=['id_venda'],keep='first')
    # Erros financeiros são sinalizados, não substituídos sem evidência.
    df['valor_recalculado_brl']=(df['quantidade']*df['preco_unitario_brl']).round(2)
    df['divergencia_financeira']=(df['valor_recalculado_brl']-df['valor_item_brl']).abs()>0.011
    df.to_csv(tratado,index=False,encoding='utf-8-sig')
    resumo={'origem':origem,'natureza':'vendas farmacêuticas; NÃO contém notificações epidemiológicas',
        'linhas_brutas':len(bruto),'colunas_brutas':len(bruto.columns),
        'datas_minima':str(bruto['Data_Venda'].min()),'datas_maxima':str(bruto['Data_Venda'].max()),
        'numero_filiais':int(bruto['ID_Filial'].nunique()),'numero_produtos':int(bruto['ID_Produto'].nunique()),
        'valor_total_brl':round(float(bruto['Valor_Total_Item_R$'].sum()),2),
        'falta_id_cliente':int(faltantes.get('ID_Cliente',0)) if 'ID_Cliente' in bruto.columns else None,
        'linhas_duplicadas':duplicatas_linhas,'ids_venda_repetidos':duplicatas_id,
        'valores_divergentes':valores_divergentes,'quantidades_ou_precos_invalidos':invalido,
        'datas_invalidas':datas_invalidas,'faltantes_por_coluna':{k:int(v) for k,v in faltantes.items()},
        'restricao':'Não permite calcular incidência, localizar focos ou inferir casos de dengue/zika/chikungunya.',
        'dados_pessoais':'ID_Cliente omitido de todos os arquivos publicáveis.'}
    out.write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding='utf-8')
    if verbose: print('Auditoria farmácia:',resumo['linhas_brutas'],'linhas, R$',resumo['valor_total_brl'])
    return df,resumo

if __name__=='__main__':
    processar(Path(__file__).resolve().parents[1])
