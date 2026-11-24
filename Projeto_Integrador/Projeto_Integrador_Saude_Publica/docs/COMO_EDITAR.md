# Como editar o dashboard

O painel está dentro da pasta `docs/`. É uma página web simples, sem frameworks ou bibliotecas externas.

| Arquivo | Para que serve |
| --- | --- |
| `index.html` | Textos, títulos, três abas, indicadores e organização da página. |
| `assets/styles.css` | Cores, fontes, tamanho e aparência das caixas e gráficos. |
| `assets/app.js` | Filtros, contas, gráficos de linha, barras, tabela e pontos clicáveis. |
| `assets/dados-painel.js` | Dados resumidos. **É gerado a partir dos CSVs e pode ser sobrescrito**. |

## O que posso mudar facilmente?

1. **Título:** procure `<h1>` em `index.html`.
2. **Texto de cada aba:** procure `<h2>` e `<h3>` em `index.html`.
3. **Cor principal:** altere `--azul` no começo do `styles.css`.
4. **Filtros:** já existem opções simples de ano, doença e bairro.
5. **Dados:** se alterar os CSVs, execute `python executar_projeto.py` na pasta principal para gerar o painel atualizado.

O código **não envia** dados a servidor. É possível testar clicando duas vezes em `docs/index.html` no seu computador ou usando a extensão Live Server no VS Code.

## Interpretação para apresentar

- **Visão geral:** comente o comportamento temporal e a diferença entre doenças.
- **Bairros:** compare as taxas por população e as ações de controle, sem afirmar causalidade.
- **Previsão:** explique que o erro médio (MAE) é medido em dados fictícios reservados para teste.

A representação de bairros usa pontos de localização **ilustrativos**. Não corresponde a um mapa real. A versão em Google Looker Studio é uma etapa separada, descrita em `documentacao/04_guia_looker_studio.md`.
