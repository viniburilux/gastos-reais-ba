# Leitura estratégica — gastos-reais-ba

**Data:** 17 de agosto de 2026  |  **Repositório:** [gastos-reais-ba](https://github.com/viniburilux/gastos-reais-ba)  |  **Autor:** Manus AI

> Este documento é uma auditoria de inventário e potencial. Ele não altera o código existente e não afirma que funcionalidades foram executadas ou validadas quando isso não aparece na evidência observada.

## Síntese executiva

Repositório de pesquisa/protótipo que entrega um dataset analítico (municipal — Bahia 2025) integrado a partir de PNCP, IBGE e SICONFI, acompanhado de um notebook de pipeline, uma aplicação Streamlit para exploração e páginas estáticas com estudo de caso. Evidências mostram um produto pesquisável e visual, mas a automação, testes, governance e artefatos de produção são limitados ou ausentes.

## Domínio e propósito aparente

Análise e monitoramento de contratações públicas municipais (foco em Bahia, contratos por inexigibilidade/contratações diretas em 2025). O objetivo declarado é transformar dados públicos fragmentados em uma camada analítica pronta para pesquisa, visualização e monitoramento.

## Indicadores do snapshot

| Indicador | Valor |
|---|---:|
| Arquivos contabilizados | 6 |
| Tamanho no snapshot | 15282132 bytes |
| Último commit observado | b6467579495e518b88b6a3b684a23e9d97b74d25	2026-07-28T05:03:10-03:00	Revise README for clarity and project focus |
| Prioridade sugerida | alta |

## Evidências observadas

- EVIDÊNCIA — pncp_ibge_siconfi_BA_final.csv (~15 MB) presente na pasta raiz: dataset analítico já gerado e versionado no repositório.
- EVIDÊNCIA — pipeline_gastos_municipais_v3.ipynb: notebook com código para coleta/integração (helpers para SICONFI/IBGE, merge, cálculos de indicadores como gasto_per_capita, instruções de pré-requisito e configuração para BA).
- EVIDÊNCIA — app.py: aplicação Streamlit que consome dados para exploração interativa (UI, rotinas de plotagem com plotly, rótulos de categorias, cores e export), instrução para rodar: `streamlit run app.py` e dependências listadas em requirements.txt.
- EVIDÊNCIA — index.html: página estática de case study (contratações artísticas Bahia 2025) com conteúdo editorial e visualização estática; README inclui URLs para GitHub Pages (explorador e monitor), indicando exploradores públicos.
- EVIDÊNCIA — requirements.txt lista dependências mínimas (streamlit, pandas, plotly, pillow, kaleido).
- EVIDÊNCIA — README.md descreve arquitetura, fontes (PNCP, IBGE, SICONFI), variáveis do dataset, escopo atual (BA, 2025, inexigibilidade) e roadmap/licença (dados: CC BY 4.0, código: MIT).
- EVIDÊNCIA — notebook contém comentário explícito: 'Os arquivos PNCP já foram coletados e classificados anteriormente.' — sinal de que a etapa de coleta PNCP não está automatizada dentro do notebook entregue (ou exige artefato externo).
- EVIDÊNCIA — não foram encontrados arquivos de CI/CD (GitHub Actions), orquestrador (Airflow/DAG), Dockerfile, Makefile, testes automatizados, ou especificação de schema (JSON Schema/Avro) no dossiê.
- INFERÊNCIA — a Streamlit app e os HTMLs indicam intenção/possibilidade de publicação pública (explorers), mas não há artefatos de deploy automatizado no repositório para comprovar pipelines de publicação contínua.

## Ativos e capacidades

- Dataset analítico integrado: pncp_ibge_siconfi_BA_final.csv (resultado final pronto para análise).
- Notebook de pipeline (pipeline_gastos_municipais_v3.ipynb) com etapas reproduzíveis documentadas para: configuração por UF, helpers de requisição robustos (retry e suporte gzip), parsing de SIDRA, merge e geração de indicadores (gasto_per_capita, gasto_pct_pib, gasto_pct_rcl).
- Aplicação interativa (Streamlit) pronta para execução local, com design, mapas/plots (plotly) e filtros, incluindo dicionários de rótulos e paletas (CAT_LABELS, SUBCAT_LABELS, CAT_COLORS).
- Página estática (index.html) com estudo de caso editorial e templates visuais para divulgação/relatórios.
- Documentação de alto nível (README) com arquitetura, fontes, variáveis, roadmap e licenças.
- Conectores/logic fragments: código para chamadas HTTP a IBGE/SICONFI e parsing de respostas (get_json, parse_sidra) que podem ser reaproveitados como conectores.
- Design e mapeamentos de categoria (categoria/cores/labels) incorporados ao app — utilidade para classificação e UX.

## Maturidade observável

Protótipo pesquisador / proof-of-concept com artefatos analíticos prontos (dataset e exploradores). Observável maturidade técnica em ciência de dados (notebook documentado, funções de requisição robustas, derivação de indicadores). Falta maturidade operacional/produtiva: ausência de automação completa da coleta PNCP no repositório, sem CI/CD, sem conteinerização, sem orquestração, sem testes automatizados, sem definição de esquema formal e metadados (catalogação). Governança de dados e avaliações de privacidade/PII não estão documentadas. Em resumo: pronto para exploração e pesquisa, não pronto como pipeline operacional/produção ou serviço de dados corporativo.

## Potencial de aproveitamento

- Integração com o ecossistema LuxVerso/GhostWorks como conector reutilizável para PNCP/IBGE/SICONFI (extrair helpers do notebook e transformar em um pacote/connector padronizado).
- Base para treinar modelos de classificação de objetos de contratação (rótulos e dataset já contêm categoria/descrições que podem ser usados como rótulos de treino).
- Expansão para cobertura nacional e modalidades adicionais: mover a lógica parametrizada do notebook para scripts/ETL sistematizados e orquestrados, gerando datasets estaduais e um dataset nacional unificado.
- Servir como camada analítica (analytical layer) para dashboards, APIs públicas e serviços de monitoramento em tempo real (por exemplo: alertas sobre concentração de fornecedores, gastos atípicos por município).
- Incorporação à plataforma de dados interna com versionamento de datasets, catálogos (Data Catalog/CKAN) e pipelines reprodutíveis (DAGs) para monitoramento contínuo.
- Uso em trabalhos de pesquisa, jornalismo de dados e auditoria exploratória — devido ao dataset já integrado e indicadores derivados.

## Riscos e lacunas

- Reprodutibilidade parcial: notebook exige CSVs PNCP já coletados (comentário explícito) — pipeline de coleta não automatizado/no código fonte público; reproduzir o dataset a partir do zero pode exigir passos manuais não documentados.
- Ausência de testes e CI: não há testes unitários, de integração, nem pipelines de CI para validar alterações no código ou nos dados.
- Falta de orquestração/automação: não há DAGs, GitHub Actions, Dockerfile, ou scripts de deploy para transformar o trabalho em processo contínuo e auditável.
- Governança de dados ausente: falta de dicionário de dados formal, esquemas, contratos de dados, versionamento de dataset (além do CSV no repositório) e políticas de retenção/linhagem.
- Segurança e privacidade não avaliadas: não há documentação sobre PII/PD (fornecedores podem conter dados pessoais), nem processos de anonimização/mascaramento ou avaliações de risco de privacidade.
- Escalabilidade/performance: notebook e Streamlit são voltados para execução local; sem conteinerização ou otimização, processos de coleta em escala nacional podem falhar por rate limits, memória ou tempo de execução.
- Dependências e ambiente: requirements.txt básico, sem bloqueio de versões (lockfile) — risco de reproducibilidade de ambiente.
- Validação de qualidade de dados limitada: não foram encontrados testes de integridade, validação de schema ou checagens automatizadas (p.ex. great_expectations).
- Deploy e observabilidade dos exploradores públicos não documentados no repositório (links no README são evidência de publicação externa, mas processo de build/deploy não está versionado aqui).

## Próximos passos recomendados

- 1) Capturar e documentar a etapa de coleta PNCP: extrair/versão do código de coleta (se existe externamente) ou implementar coleta parametrizada no repositório (script CLI) para tornar o pipeline reprodutível a partir de origem pública.
- 2) Modularizar o notebook: mover lógica crítica (get_json, parse_sidra, merges, cálculos de indicadores) para pacotes/scripts Python versionados (src/), com funções testáveis e parâmetros (UF, ano, rate-limit).
- 3) Definir e publicar um esquema de dados e dicionário (ex.: JSON Schema, Data Catalog entry) para pncp_ibge_siconfi_BA_final.csv; incluir exemplos de linhas e tipos/validações e critérios de qualidade.
- 4) Adotar CI/CD básico: GitHub Actions para rodar lint, testes unitários, validação de schema e builds de artefatos (ex.: CSV de teste); criar job que faça smoke tests no Streamlit/app build-step.
- 5) Implementar validação de dados automatizada (p.ex. great_expectations ou tests pytest com casos de borda) e checagens pós-merge (uniques, chaves, NAs esperados).
- 6) Conteinerizar a aplicação e pipeline (Dockerfile) e documentar execução reproduzível (makefile ou scripts run/).
- 7) Preparar orquestração/execução automatizada (Airflow, Prefect ou GitHub Actions + scheduled runs) com controle de rate-limiting e retries, logging centralizado e alertas em falhas.
- 8) Realizar revisão de privacidade e segurança dos dados: inventariar campos com PII, aplicar mascaramento/anonymization no dataset público quando necessário e documentar justificativas sob a licença CC BY 4.0.
- 9) Adotar versionamento de dados (DVC/Delta/MLFlow ou storage versioning) e publicar metadados no catálogo de dados do LuxVerso/GhostWorks para facilitar reuso e discovery.
- 10) Extração de conectores reutilizáveis: empacotar chamadas a IBGE/SICONFI/PNCP como módulos de GhostWorks para integração com outros projetos, acompanhado de exemplos e testes de integração limitados (mocked).
- 11) Planejar monitoramento/observabilidade do pipeline: métricas de ingestão, taxas de erro, coverage de dados por município e alertas para mudanças significativas nos esquemas de fontes externas.
- 12) Documentar o processo de deploy dos explorers públicos (passos para atualizar GitHub Pages / hosting) e incluir scripts/automation para publicação reproducível.

## Método e limites

A leitura foi feita sobre um snapshot de profundidade 1 e sobre arquivos textuais selecionados por relevância estrutural, incluindo README, manifests e amostras de código. Dependências, notebooks, binários, dados grandes e integrações externas podem exigir uma rodada posterior de execução controlada. Nenhum código do repositório foi executado durante a auditoria.

**Fonte primária:** [gastos-reais-ba](https://github.com/viniburilux/gastos-reais-ba)
