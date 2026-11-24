-- Consultas SQLite para VS Code / DB Browser. Apenas dados SINTÉTICOS na tabela de saúde.
-- 1. Casos por doença
SELECT doenca, SUM(casos_notificados) AS notificacoes_ficticias
FROM fato_notificacoes GROUP BY doenca ORDER BY notificacoes_ficticias DESC;

-- 2. Bairros com mais notificações/100 mil habitantes NO PERÍODO (não é taxa anual)
SELECT bairro, SUM(casos_notificados) AS total_notificacoes,
       ROUND(100000.0 * SUM(casos_notificados) / MAX(populacao_simulada), 2) AS notificacoes_100mil_periodo
FROM fato_notificacoes GROUP BY bairro ORDER BY notificacoes_100mil_periodo DESC;

-- 3. Série mensal: todas as doenças
SELECT ano_mes, doenca, SUM(casos_notificados) AS casos
FROM fato_notificacoes GROUP BY ano_mes, doenca ORDER BY ano_mes, doenca;

-- 4. Somar focos sem triplicar devido ao cruzamento por doença
SELECT bairro_id, SUM(focos_identificados) AS focos_total
FROM (SELECT DISTINCT bairro_id, semana_inicio, focos_identificados FROM fato_notificacoes)
GROUP BY bairro_id ORDER BY focos_total DESC;

-- 5. Farmácia em contexto separado; NÃO permite medir casos ou incidência.
SELECT categoria, COUNT(*) AS itens_transacionados, SUM(valor_item_brl) AS faturamento_brl
FROM fato_vendas_farmacia GROUP BY categoria ORDER BY faturamento_brl DESC;
