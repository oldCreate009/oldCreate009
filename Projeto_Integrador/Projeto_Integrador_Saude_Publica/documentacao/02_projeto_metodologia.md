# Plano de pesquisa e metodologia (ABP)

## Contexto do problema

A Situação-Problema 2 propõe que uma Secretaria Municipal de Saúde analise dengue, zika e chikungunya utilizando casos notificados, localização geográfica, chuva, focos do vetor e ações de controle. Essas informações permitem identificar tendências e subsidiar a alocação de visitas, mutirões e ações educativas, mas não são automaticamente evidência causal.

## Questões de pesquisa

1. Quais bairros têm maiores taxas de notificações de arboviroses, ajustadas pela população simulada?
2. Como as notificações variam ao longo das semanas/meses do estudo?
3. Que padrões exploratórios existem entre chuva, focos e notificações?
4. Quais grupos de bairros apresentam perfis semelhantes de notificações, chuvas e focos?
5. Um modelo simples prediz o número de notificações semanais melhor que o baseline de persistência?

## ABP (Aprendizagem Baseada em Problemas)

- Identificar: obstáculos da Secretaria em relacionar indicadores no tempo e no espaço.
- Pesquisar: conceitos de incidência/notificação, qualidade de dados, ETL, análise espacial, Big Data e privacidade.
- Desenvolver: scripts, relatórios, banco SQLite, previsão experimental e dados de dashboards.
- Apresentar e defender: narrativa de problema, metodologia, dados, achados e limitações.

## Origem de cada dado (proveniência)

| Fonte | Granularidade | Origem | Tratamento correto |
|---|---|---|---|
| Vendas farmacêuticas (arquivo do estudante) | item de venda em farmácia | CSV ORIGINAL, 50 vendas | somente contexto varejista, **não** casos |
| Notificações dengue, zika, chikungunya | bairro-semana-doença | SIMULAÇÃO | resultado didático, não epidemiológico |
| População de bairro | bairro | SIMULAÇÃO | denominador fictício dos indicadores |
| Precipitação e temperatura | bairro-semana | SIMULAÇÃO | covariáveis fictícias |
| Focos de mosquito | bairro-semana | SIMULAÇÃO | fator contextual fictício |
| Visitas/mutirões/focos eliminados | bairro-semana | SIMULAÇÃO | ação pública fictícia |

## Processo ETL

1. Auditoria: leitura do CSV original em codificação `cp1252`; 50 transações, 14 colunas e 12 IDs de cliente ausentes; nenhuma transação duplicada. Remoção de ID de cliente das saídas públicas.
2. Coleta sintética: gerador determinístico com seed 42; 6 bairros, 104 semanas e três doenças. Não se insere caso epidemiológico extraído da farmácia.
3. Tratamento: validação de chave `bairro_id + semana_inicio + doenca`, integração `many_to_one` das fontes ambientais, prevenção de multiplicação de focos por doença.
4. Engenharia de atributos: mês, ano, taxa por 100 mil habitantes, chuva defasada 2 semanas, focos 1 semana, visitas 2 semanas, médias móveis e contagens passadas.
5. Carregamento: CSV UTF-8 e banco SQLite gerado localmente.

## Indicadores / definições

- `notificacoes_por_100mil_periodo = SUM(casos_notificados) / populacao_simulada × 100000` **para o período inteiro**; não representa risco anual.
- `casos_notificados` é total de registros sintéticos, não pessoas únicas.
- `focos_total` e `visitas_total`: somam por bairro e semana após excluir duplicação causada pelas três doenças.
- `chuva_media_mm`: média por bairro/semana; cuidado com agregações adicionais.
- `cluster_exploratorio`: classificação de similaridade por KMeans, **não é diagnóstico nem ranking médico**.
- Previsões: contagens não negativas geradas por Random Forest. Todas são meramente experimentais.

## Técnicas espaciais/temporais

Análise temporal: série mensal, média móvel de 6 semanas e comparação sazonal descritiva. Análise espacial: razão de notificações/população, distribuição nos centróides ilustrativos e clustering KMeans de atributos agregados. Mapas de calor podem ser demonstrados na etapa do dashboard, mas são ilustrativos porque os bairros e as coordenadas são fictícios. **Geoestatística inferencial (Moran I, Kriging) não foi aplicada**, pois 6 centróides simulados não sustentam validação territorial real.

## Modelo e validação

RandomForestRegressor, com categorias de bairro/doença e fatores apenas passados; treino de 2024-01 até antes de 2025-07-07; teste de 2025-07-07 a 2025-12. Baseline: notificações na semana anterior. Métricas MAE, RMSE, WAPE; estimativas retrospectivas, não um sistema operacional para emissão de alertas.

## Storytelling para gestor municipal

Primeiro, caracterizar a evolução das notificações; depois comparar taxas padronizadas entre bairros; em seguida relacionar fatores ambientais de forma exploratória e comunicar esforços de controle. Por último, mostrar a comparação experimental de previsões contra valores simulados e enfatizar que decisões reais exigem registros verdadeiros, validação externa e critérios epidemiológicos.
