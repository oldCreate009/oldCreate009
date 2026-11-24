# Limitações, fontes, privacidade e ética

## O que o arquivo de origem autoriza afirmar

Foram fornecidas 50 linhas de transações de farmácia; o conteúdo inclui categoria de produtos, preço, data, filiais e IDs de clientes. A presença de antitérmicos **não autoriza** inferir diagnósticos de dengue, zika ou chikungunya. Farmácias podem refletir consumo por muitas causas, não a incidência de uma doença específica. O arquivo não tem município confirmado nem população de referência.

## O que é simulado

Os conjuntos `bairros`, `clima_semanal`, `focos_semanal`, `acoes_controle_semanal` e `casos_notificados_semanais` são inventados por um gerador determinístico com seed 42. Cada registro de saúde está marcado como `SINTETICO_EDUCACIONAL`. O modelo pode aprender as regras usadas na geração, o que não prova generalização real.

## Problemas que precisariam ser solucionados com dados oficiais

- Definir município, bairros/códigos geográficos e período de vigilância.
- Obter casos notificados com critérios de definição e datas coerentes, preferindo agregados para preservar privacidade.
- Definir população residente por bairro ou área para calcular taxas; atualizar denominadores no tempo, quando possível.
- Integrar chuva por estação/área/semana, discutindo distâncias e defasagens.
- Acessar dados de focos e controle vetorial com classificação de ações e cobertura.
- Revisar casos duplicados, atraso de notificação, subnotificação e mudanças de definição de caso.
- Validar externamente modelos e limitações antes de recomendações operacionais.

## Fontes públicas para pesquisa futura (não foram usadas para gerar os casos deste projeto)

- Ministério da Saúde — OpenDataSUS: https://opendatasus.saude.gov.br/
- INMET — séries históricas anuais: https://portal.inmet.gov.br/dadoshistoricos/
- INMET — BDMEP: https://bdmep.inmet.gov.br/
- Portal de dados da secretaria estadual/municipal de saúde do local escolhido (a definir).

A disponibilidade, licença, granularidade e proteção de dados precisam ser verificadas antes da coleta. Não foram baixados registros de pacientes.

## LGPD e privacidade

A pasta `dados/00_original_privado` é local e ignorada no GitHub; mantém o arquivo original sem modificações. Todas as saídas publicáveis removem a coluna `ID_Cliente`. Nenhuma base do projeto contém cadastro real de paciente. Se dados de saúde reais forem incorporados, **não publique linhas identificáveis** nem detalhes de geolocalização individual; trabalhe com agregados e observe a legislação e políticas do fornecedor.

## Limitações do projeto atual

**Não satisfaz empiricamente a parte do cenário que pressupõe dados reais de notificação, focos e intervenções locais**; demonstra as técnicas com dados simulados. Mapas são ilustrativos. A associação chuva×casos não permite declarar causalidade. O período tem só 104 semanas; as taxas no período não devem ser apresentadas como anuais. O dashboard do Looker Studio será concluído em conjunto com o estudante.
