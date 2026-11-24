# Dicionário de dados e chaves

## `dados/02_simulados/casos_notificados_semanais.csv`

- `semana_inicio` (data `YYYY-MM-DD`): segunda-feira da semana de referência.
- `bairro_id` (texto): chave fictícia de bairro, B01 a B06.
- `doenca` (categoria): Dengue, Chikungunya ou Zika.
- `casos_notificados` (inteiro): contagem de notificações **fictícias** (não pessoas únicas).
- `origem_dados` (texto): `SINTETICO_EDUCACIONAL`.
- **Chave:** `semana_inicio + bairro_id + doenca`.

## `bairros.csv`

- `bairro_id`, `bairro`: bairro fictício e chave.
- `populacao_simulada`: denominador inventado, constante no período.
- `latitude_ilustrativa`, `longitude_ilustrativa`: centroide fictício para testar o mapa, NÃO localização real.

## `clima_semanal.csv`

- `semana_inicio + bairro_id`: chave composta.
- `chuva_mm_semana`: precipitação acumulada estimada em mm, **simulada**.
- `temp_media_c`: temperatura média semanal em °C, **simulada**.

## `focos_semanal.csv`

- `focos_identificados`: contagem fictícia semanal de focos encontrados.

## `acoes_controle_semanal.csv`

- `visitas_agentes`: visitas fictícias de agentes.
- `mutiroes`: número fictício de mutirões.
- `focos_eliminados`: contagem fictícia de focos eliminados.

## `dados/03_tratados/saude_bairro_semana_doenca.csv`

Junção de notificações × `clima` × `focos` × `ações` × `bairros`, sempre em granularidade de **bairro + semana + doença**.

- `ano`, `mes`, `ano_mes`, `semana_iso`: campos temporais.
- `incidencia_100mil_semana`: nome técnico no script, representa **notificações semanais por 100 mil habitantes** do cenário fictício, não casos confirmados nem incidência real.
- `casos_lag1`, `casos_lag2`, `casos_lag4`: contagens da mesma doença/bairro 1, 2, 4 semanas antes.
- `media_movel_4s`: média das 4 semanas **anteriores**, não inclui semana atual.
- `chuva_lag2`, `focos_lag1`, `visitas_lag2`, `temp_lag1`: valores defasados, para evitar usar informações futuras na previsão.
- `tipo_dados`: `SIMULADO_FICTICIO`.

## `dados/04_dashboard/*.csv`

- `01_serie_mensal_doencas`: mês-doença, total de notificações.
- `02_mapa_bairros`: bairro (6 linhas), coordenadas simuladas, população, notificações, focos, visitas, mutirões, taxa em todo o período, cluster.
- `03_doencas_por_bairro`: bairro-doença (18 linhas) com notificações e taxa por população.
- `04_detalhe_epidemiologico`: 1.872 linhas bairro-semana-doença.
- `05_contexto_farmacia_separado`: categorias de vendas de farmácia **sem relação epidemiológica demonstrada**.
- `06_previsoes_teste_temporal`: série observada x previsão, apenas no conjunto de teste temporal.

**Alerta de agregação:** `clima`, `focos` e `ações` se repetem **três vezes** em `04_detalhe_epidemiologico.csv` (uma por doença). Não some focos/visitas dessa tabela sobre todas as doenças sem deduplicação. Use `02_mapa_bairros.csv` para totais de focos e visitas. Também evite somar população do bairro a cada linha.
