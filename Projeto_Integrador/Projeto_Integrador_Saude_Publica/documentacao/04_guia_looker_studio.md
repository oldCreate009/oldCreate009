# Dashboard no Google Looker Studio

**Situação:** o dashboard **HTML** das três abas está pronto em `docs/`, podendo ser hospedado no GitHub Pages. A versão no **Google Looker Studio** ainda não foi criada, pois requer o acesso do estudante à sua conta.

O PDF da disciplina solicita explicitamente o Google Looker Studio. Portanto, o site HTML **não substitui** essa etapa.

## Arquivos para importar

| Arquivo CSV em `dados/04_dashboard/` | O que mostra |
| --- | --- |
| `01_serie_mensal_doencas.csv` | Notificações por mês e por doença (gráfico de linhas). |
| `02_mapa_bairros.csv` | Bairros fictícios, população, taxas, focos, visitas e coordenadas ilustrativas. |
| `03_doencas_por_bairro.csv` | Notificações por bairro e doença (barras). |
| `04_detalhe_epidemiologico.csv` | Análise semanal e filtros de data/bairro/doença. |
| `06_previsoes_teste_temporal.csv` | Observado x previsto e erros do modelo. |

O arquivo `05_contexto_farmacia_separado.csv` é apenas a auditoria da farmácia. Não deve ser combinado com casos de arbovirose.

## Como montar três páginas simples

1. Importe cada CSV para uma aba do Google Sheets (verifique formato de data e UTF-8).
2. Em https://lookerstudio.google.com/, crie um relatório e adicione as planilhas como fontes.
3. **Página 1: Visão geral** — linhas de `ano_mes` x `casos_notificados` por `doenca`; barras por doença e cartões.
4. **Página 2: Bairros** — barras de `notificacoes_por_100mil_periodo` e tabela de `focos_total` e `visitas_total`. Se usar mapa, configure `latitude_ilustrativa` e `longitude_ilustrativa` como coordenadas, com aviso de que são fictícias.
5. **Página 3: Previsão** — duas linhas por `semana_inicio`, somando `casos_notificados` e `previsto_modelo` da base de teste; comentário sobre MAE do modelo.
6. Adicione filtros de período, bairro e doença nas páginas em que a fonte utilizada contenha esses campos.
7. Inclua a mensagem **DADOS SINTÉTICOS — CENÁRIO EDUCACIONAL** visível em todas as páginas.
8. Compartilhe o relatório com permissão de leitura e adicione o link no README do GitHub.

## Cuidados na interpretação

- Não some focos de `04_detalhe_epidemiologico.csv` diretamente: os valores se repetem por doença. Para totais de focos, use `02_mapa_bairros.csv` (total por bairro) ou deduplique por semana e bairro antes de agregar.
- Os pontos geográficos são **ilustrativos** e não representam residências ou focos reais.
- Os indicadores do teste preditivo são de dados fictícios e não comprovam desempenho em situações reais.

**Link do Looker Studio:** [inserir depois de criar]

Documentação oficial: https://cloud.google.com/looker/docs/studio/
