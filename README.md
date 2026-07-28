# LuxVerso Public Procurement Analytics

```
           PNCP
             │
             ▼
     Data Collection
             │
             ▼
 Data Cleaning & Classification
             │
             ▼
      IBGE Integration
             │
             ▼
    SICONFI Integration
             │
             ▼
 Analytical Dataset
             │
             ▼
 Dashboards • Research • Monitoring
```

Open analytical infrastructure for exploring Brazilian municipal public procurement through integrated public datasets.

LuxVerso Public Procurement Analytics is an open research initiative that transforms fragmented government data into analysis-ready datasets for studying municipal procurement.

The project integrates information from the **Portal Nacional de Contratações Públicas (PNCP)**, **IBGE** and **SICONFI**, creating a unified analytical layer for public finance research, transparency initiatives and exploratory data analysis.

The current public repository presents the first implementation of this infrastructure using municipal direct procurement contracts from **Bahia (2025)**.

---

# Why this project exists

Brazilian procurement data is publicly available, but it is distributed across multiple government systems and difficult to analyze at scale.

LuxVerso Public Procurement Analytics automates the complete analytical workflow by:

- collecting procurement records from the PNCP API;
- cleaning and standardizing government data;
- classifying procurement objects;
- integrating demographic indicators from IBGE;
- integrating municipal fiscal indicators from SICONFI;
- generating analytical datasets ready for research and visualization.

Instead of exposing raw government records, the project provides a structured analytical layer that supports exploration and comparative analysis.

---

# Data Pipeline

The current pipeline performs:

- Automatic data collection from the PNCP API
- Data normalization and validation
- Procurement object classification
- Municipal identification
- Integration with IBGE indicators
- Integration with SICONFI fiscal information
- Generation of analysis-ready datasets

The pipeline architecture was designed to support continuous monitoring and future expansion to additional procurement modalities and all Brazilian states.

---

# Current Public Dataset

The repository currently includes an analytical dataset covering **municipal direct procurement contracts in Bahia during 2025**.

Integrated sources include:

- Portal Nacional de Contratações Públicas (PNCP)
- Instituto Brasileiro de Geografia e Estatística (IBGE)
- Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro (SICONFI)

Each record combines the original procurement information with contextual socioeconomic and fiscal indicators.

Variables include:

- procurement information
- municipality identifiers
- supplier information
- contract values
- contract classification
- municipal population
- GDP
- GDP per capita
- fiscal revenue
- public expenditure indicators
- derived analytical metrics

---

# Example Research Questions

The current dataset enables analyses such as:

- Which municipalities spend more per capita through direct procurement?
- Which suppliers appear across multiple municipalities?
- How concentrated are procurement contracts?
- How does procurement vary with municipal population?
- Is procurement associated with municipal fiscal capacity?
- Which municipalities allocate a larger share of revenue to specific procurement categories?
- How do procurement patterns evolve over time?

These examples illustrate only part of the analytical possibilities created by integrating multiple public datasets.

---

# Public Explorers

## Municipal Procurement Explorer

https://viniburilux.github.io/explorador-dados-bahia/

Interactive exploration of procurement data, including:

- municipalities
- suppliers
- procurement categories
- contract values
- spending evolution
- contract classification

---

## Public Finance Monitor

https://viniburilux.github.io/monitor-gastos-pncp/

Overview of the analytical infrastructure and exploratory findings produced from the integrated datasets.

---

# Repository Structure

```
data/
    pncp_ibge_siconfi_BA_final.csv

pipeline/
    data collection
    normalization
    integration

docs/
    public dashboards
```

---

# Data Sources

### Portal Nacional de Contratações Públicas (PNCP)

Primary source of procurement contracts.

https://www.gov.br/pncp

---

### IBGE

Municipal demographic and socioeconomic indicators.

https://www.ibge.gov.br

---

### SICONFI — Tesouro Nacional

Municipal fiscal indicators.

https://siconfi.tesouro.gov.br

---

# Current Scope

Current public implementation:

- Bahia
- Municipal procurement
- Direct procurement (Inexigibilidade)
- 2025

The underlying infrastructure has been designed for continuous data collection and future expansion to additional procurement categories, years and Brazilian states.

---

# Roadmap

Current public implementation:

- ✅ Bahia analytical dataset
- ✅ PNCP integration
- ✅ IBGE integration
- ✅ SICONFI integration
- ✅ Public exploratory dashboards

Next development stages:

- National procurement dataset
- Continuous monitoring pipeline
- Additional procurement modalities
- Public APIs
- Advanced analytical dashboards

---

# Potential Applications

The project may support:

- public finance research
- procurement monitoring
- municipal benchmarking
- transparency initiatives
- data journalism
- academic research
- exploratory auditing
- public policy analysis

---

# About LuxVerso

LuxVerso develops open analytical infrastructures for exploring complex public datasets through automated collection, integration and analysis.

Current research areas include:

- public procurement analytics
- municipal finance
- government open data
- analytical data infrastructure
- computational social science

---

# License

### Data

CC BY 4.0

### Code

MIT License

---

# Contact

**Vinícius Buri**

LuxVerso Research

Salvador — Bahia — Brazil

viniburilux@gmail.com
