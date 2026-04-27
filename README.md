# LuxVerso Public Finance
Monitor automatizado de contratos públicos diretos  
Bahia · 2025–2026

LuxVerso Public Finance é uma infraestrutura experimental de análise de contratações públicas municipais baseada em dados abertos do governo brasileiro.

O sistema coleta automaticamente dados do **Portal Nacional de Contratações Públicas (PNCP)** e os organiza em datasets analíticos que permitem explorar padrões de gasto público em escala municipal.

A primeira implementação analisa contratos de **inexigibilidade de licitação** nos municípios da Bahia entre 2025 e 2026.

---

## O que o sistema faz

O pipeline desenvolvido realiza:

1. Coleta automática de contratos via API do PNCP
2. Normalização e limpeza de dados
3. Classificação de contratos por categoria
4. Integração com indicadores socioeconômicos (IBGE)
5. Integração com dados fiscais municipais (SICONFI)
6. Geração de datasets analíticos exploráveis

Isso permite analisar contratos públicos dentro do contexto econômico e fiscal de cada município.

---

## Exploradores públicos

Duas interfaces públicas permitem explorar os dados.

### Explorador de contratos artísticos

https://viniburilux.github.io/explorador-dados-bahia/

Permite explorar:
- municípios que mais gastam em shows
- artistas contratados em múltiplas cidades
- evolução mensal de gastos
- cachês individuais

### Monitor de gastos públicos

https://viniburilux.github.io/monitor-gastos-pncp/

Apresenta a infraestrutura de coleta e os principais achados iniciais sobre contratos municipais.

---

## Estrutura dos dados

O repositório contém o dataset analítico utilizado nas análises públicas.

Dataset principal:

```
data/pncp_ibge_siconfi_BA_final.csv
```

Esse dataset inclui:
- contratos do PNCP
- classificação de objeto
- identificação municipal
- indicadores populacionais
- indicadores fiscais

---

## Sobre os números apresentados

Os números do projeto variam conforme o **escopo analítico utilizado**.

| Escopo | Contratos |
|---|---|
| Dataset bruto PNCP | ~28.306 contratos |
| Dataset municipal filtrado | ~21.797 contratos |
| Dataset limpo analisado | ~14.275 contratos |

As diferenças refletem:
- remoção de registros não municipais
- remoção de duplicações
- identificação de outliers
- classificação de contratos relevantes

Todos os critérios estão documentados no notebook de metodologia.

---

## Fontes de dados

**Portal Nacional de Contratações Públicas (PNCP)**  
https://www.gov.br/pncp  
Fonte primária de contratos públicos.

**IBGE**  
https://www.ibge.gov.br  
Indicadores municipais para contextualização socioeconômica.

**SICONFI – Tesouro Nacional**  
https://siconfi.tesouro.gov.br  
Dados fiscais para contextualizar capacidade orçamentária municipal.

---

## Status do projeto

Este repositório representa a primeira implementação do sistema para o estado da Bahia.

Próximas etapas:
- expansão para outros estados brasileiros
- monitoramento contínuo de contratos
- detecção automatizada de padrões de gasto
- API pública para exploração dos dados

---

## Sobre o LuxVerso

LuxVerso é uma iniciativa independente de pesquisa aplicada focada em explorar grandes sistemas de dados públicos.

Áreas atuais:
- análise de gastos públicos municipais
- integração de datasets governamentais
- análise automatizada de contratos públicos

---

## Licença

Dados: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
Código: [MIT License](https://opensource.org/licenses/MIT)

---

## Contato

Vinícius Buri  
LuxVerso Research · Salvador, Bahia  
viniburilux@gmail.com
