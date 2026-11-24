# Implantação e monitoramento — etapa 8 (opcional)

A implantação NÃO foi realizada. Proposta de implantação futura para a Secretaria de Saúde, condicionada à obtenção de dados oficiais e avaliação técnica:

1. Agendar aquisições e ETL semanalmente, guardando log de extração, taxa de registros inválidos e cobertura por área.
2. Armazenar apenas dados necessários, com anonimização/agregação e controles de acesso.
3. Monitorar atrasos de notificação, alterações de esquema, faltantes e mudanças na população de referência.
4. Fazer atualização periódica do dashboard por fonte verificada, com legenda de atualização e proveniência.
5. Reavaliar mensalmente MAE e RMSE contra um baseline, incluindo quebra por bairro e doença.
6. Submeter resultados a epidemiologistas e gestores, evitando decisões automáticas sem revisão humana.
7. Criar auditoria de mudanças de código (Git), responsáveis e plano de resposta a falhas.

Por se tratar de protótipo educacional, nenhuma ação operacional ou monitoramento real está ativo.
