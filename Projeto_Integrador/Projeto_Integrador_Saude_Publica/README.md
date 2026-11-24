# Projeto Integrador - Análise de Dados em Saúde Pública

**Situação-Problema 2:** estudo didático sobre dengue, zika e chikungunya, seguindo o ciclo de dados (extração, tratamento, análise, modelagem, avaliação e visualização).

> **Importante:** o CSV fornecido originalmente contém vendas de farmácia, **não** notificações epidemiológicas. Por isso ele foi auditado separadamente. O cenário usado para o painel (doenças, bairros, clima, focos e ações) é **inteiramente simulado**, sem validade para decisões reais de saúde pública. Se a atividade exigir dados reais, será necessário substituir essas bases por dados oficiais.

## O que tem no projeto

| Pasta | Conteúdo |
| --- | --- |
| `codigo/` | Scripts Python numerados de auditoria, simulação, ETL, análises, modelo, banco e preparação do painel. |
| `dados/01_publico/` | CSV da farmácia sem identificador de cliente, separado da análise epidemiológica. |
| `dados/02_simulados/` | Tabelas fictícias com casos, bairros, clima, focos e controle. |
| `dados/03_tratados/` | Dados limpos e integrados. |
| `dados/04_dashboard/` | CSVs finais para gráficos e Google Looker Studio. |
| `sql/` | Consultas para verificar indicadores no SQLite. |
| `graficos/` | Gráficos básicos da análise exploratória. |
| `modelos/` | Métricas da avaliação, teste temporal e referência. |
| `docs/` | **Dashboard HTML interativo**, simples e editável. |
| `documentacao/` | Etapas, dicionário, limitações, orientações para GitHub e Looker Studio. |
| `testes/` | Verificações de integridade dos dados e do painel. |

## Ver o dashboard

Abra `docs/index.html` com seu navegador. **Não é necessário instalar bibliotecas para visualizar o painel.**

Ele tem três abas:

1. **Visão geral:** total de notificações, focos, visitas, evolução mensal e comparação por doença.
2. **Bairros:** taxas por população, pontos ilustrativos clicáveis e tabela de controle vetorial.
3. **Previsão:** evolução de observado x previsto e comparação de erros no conjunto de teste.

Use os filtros de ano, doença e bairro. O painel pode ser publicado pelo GitHub Pages. Para modificá-lo, leia `docs/COMO_EDITAR.md`.

## Executar os códigos no VS Code

Abra esta pasta no VS Code, depois no terminal:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python executar_projeto.py
python -m pytest -q testes/
```

Os scripts **não** precisam de internet e conseguem reproduzir a base sintética e o painel.

A execução segue: auditoria do CSV original, dados simulados, ETL, análise exploratória, modelo, avaliação, SQLite e preparação do painel HTML. Para ver as tabelas, abra os CSVs no editor. O banco `dados/projeto_saude.db` é gerado localmente.

## Publicar no GitHub

Consulte `documentacao/03_publicar_github.md` para os comandos e a publicação do painel no **GitHub Pages**, selecionando a branch `main` e a pasta `/docs`.

**Não publique** o CSV bruto com IDs de clientes, o PDF do professor ou arquivos privados. O `.gitignore` ajuda a impedir o envio desses arquivos. Confira `git status` antes de publicar.

## Relação com a atividade

- Problema da Secretaria de Saúde: análise de arboviroses e apoio ao controle vetorial (**simulação didática**).
- Padrões temporais: evolução mensal no painel.
- Padrões territoriais: taxas por bairro e representação **esquemática**, não mapa geográfico verdadeiro.
- Análises: Python, Pandas, SQL, agrupamento, previsão e avaliação.
- Comunicação: dashboard interativo em HTML para GitHub Pages **concluído**; painel equivalente no **Google Looker Studio ainda precisa ser criado na conta do estudante**, pois é a ferramenta explicitamente solicitada no PDF.

A matriz `documentacao/01_matriz_requisitos.md` mostra cada requisito e a evidência correspondente.

## Personalizações antes da entrega

- Ajuste o título, os textos e as cores do painel no HTML e no CSS.
- Revise as observações e as interpretações dos gráficos com seus próprios comentários.
- Inclua seu nome, turma e o link do relatório do Looker Studio se ele for solicitado pelo professor.

**Cuidado:** não apresente os números simulados como estatísticas oficiais. Nenhum arquivo de relatório acadêmico formal foi incluído neste pacote.
