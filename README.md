# LuxVerso Public Procurement Analytics

Open infrastructure for municipal public procurement analysis in Brazil.

LuxVerso Public Finance is an open research initiative that integrates multiple Brazilian public datasets into a unified analytical database for exploring municipal public spending.

The project combines data from the National Public Procurement Portal (PNCP), IBGE and SICONFI to create contextualized datasets that enable large-scale analyses of municipal procurement.

The current public release focuses on direct public contracts (Inexigibilidade de Licitação) in the state of Bahia.

---

## Why this project exists

Public procurement data is publicly available, but it is fragmented across multiple government systems and difficult to analyze at scale.

LuxVerso Public Finance automates the entire process of:

- collecting procurement data
- cleaning and standardizing records
- classifying contracts
- integrating socioeconomic indicators
- integrating municipal fiscal indicators
- generating analytical datasets ready for exploration

Instead of providing raw government data, the project provides a structured analytical layer over Brazilian public finance.

---

# Data Pipeline

The current pipeline performs:

- Automatic collection from the PNCP API
- Data normalization
- Contract classification
- Municipal identification
- Integration with IBGE indicators
- Integration with SICONFI fiscal data
- Generation of analysis-ready datasets

The pipeline was designed to support continuous monitoring and expansion to all Brazilian states.

---

# Current Dataset

The public repository currently includes an analytical dataset covering municipalities in Bahia.

Integrated sources include:

- PNCP
- IBGE
- SICONFI

Variables include:

- procurement information
- municipality identifiers
- supplier information
- contract values
- population
- GDP
- GDP per capita
- fiscal revenue
- public expenditure indicators
- derived spending metrics

---

# Example Research Questions

The current dataset enables analyses such as:

- Which municipalities spend more per capita?
- Which suppliers appear across multiple municipalities?
- How concentrated are direct public contracts?
- How does procurement vary with municipal population?
- Is procurement associated with fiscal capacity?
- Which municipalities spend a larger share of revenue through direct contracting?
- How do procurement patterns evolve over time?

These examples illustrate only part of the analytical possibilities created by integrating multiple public datasets.

---

# Public Explorers

## Municipal Procurement Explorer

https://viniburilux.github.io/explorador-dados-bahia/

Interactive exploration of municipal procurement data including:

- municipalities
- suppliers
- contract values
- spending evolution
- contract classification

---

## Public Finance Monitor

https://viniburilux.github.io/monitor-gastos-pncp/

Overview of the data infrastructure and exploratory analyses built from the integrated datasets.

---

# Repository Structure

```
data/
    pncp_ibge_siconfi_BA_final.csv

pipeline/
    data collection
    normalization
    integration
```

---

# Data Sources

### Portal Nacional de Contratações Públicas (PNCP)

Primary source of procurement contracts.

https://www.gov.br/pncp

---

### IBGE

Municipal demographic and economic indicators.

https://www.ibge.gov.br

---

### SICONFI — Tesouro Nacional

Municipal fiscal indicators.

https://siconfi.tesouro.gov.br

---

# Current Scope

Current public implementation:

- Bahia
- Direct procurement (Inexigibilidade)
- Municipal contracts
- 2025–2026

The underlying infrastructure was designed to support expansion to additional procurement modalities and all Brazilian states.

---

# Potential Applications

The project may support:

- public finance research
- data journalism
- transparency initiatives
- procurement monitoring
- municipal benchmarking
- public policy analysis
- academic research
- exploratory auditing

---

# About LuxVerso

LuxVerso develops open infrastructures for exploring complex public datasets through automated data collection, integration and analysis.

Current areas include:

- public procurement
- municipal finance
- government open data
- analytical data infrastructure

---

# License

Data

CC BY 4.0

Code

MIT License

---

# Contact

Vinícius Buri

LuxVerso Research

Salvador — Bahia — Brazil

viniburilux@gmail.com
