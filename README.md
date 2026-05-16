# Sistema Inteligente de Predicao de Surtos de Dengue - Recife

Plataforma analitica para previsao de picos epidemiologicos de dengue em Recife, utilizando correlacao entre dados historicos de saude e variaveis climaticas.

## Visao Geral

Este projeto foi desenvolvido para fornecer subsidios a orgaos de saude publica na antecipacao de acoes de controle vetorial e alocacao de recursos hospitalares, atraves de predicoes com antecedencia de 4 a 8 semanas.

## Caracteristicas Tecnicas

- Pipeline completo de ETL para dados epidemiologicos e climaticos
- Feature engineering temporal com lags e medias moveis
- Modelo de regressao Ridge com validacao temporal
- Metricas: MAE de 10.86 casos/dia e R2 de 0.629
- API REST com FastAPI e MongoDB
- 20.947 casos de dengue processados (2020-2025)
- 93 bairros mapeados com georreferenciamento oficial

## Fluxo do Projeto

DADOS BRUTOS → ETL → MODELO ML → API REST → FRONTEND
↓ ↓ ↓ ↓
SINAN MongoDB .pkl file JSON/HTTP
INMET 8.4k+ Ridge FastAPI
GeoJSON registros Regression

### Pipeline Detalhado
EXTRACAO
├── Casos dengue (SINAN 2020-2025)
├── Dados clima (INMET)
└── Mapeamento bairros (Portal Dados Abertos Recife)

TRANSFORMACAO
├── Consolidacao temporal (semanal)
├── Conversao codigos → nomes bairros
├── Integracao dengue + clima
└── Feature engineering (lags, medias moveis)

MODELO ML
├── Treino: Ridge Regression
├── Validacao: Time Series Split
└── Teste: MAE 10.86 | R2 0.629

CARGA
├── MongoDB: casos_dengue (157 docs)
├── MongoDB: casos_por_bairro (8.402 docs)
└── Modelo: modelo_dengue_emprel_producao.pkl

API REST
└── 10 endpoints funcionais

## Estrutura do Projeto

projeto-dengue-recife/
├── api/
│ ├── main.py # API FastAPI (10 endpoints)
│ ├── database.py # Conexao MongoDB
│ └── models.py # Schemas Pydantic
├── data/
│ ├── raw/ # Dados brutos (nao versionados)
│ │ ├── casos-de-dengue-2020.csv ate 2025.csv
│ │ ├── dados_clima_inmet_recife.csv
│ │ └── clima_2020.zip ate 2024.zip
│ └── processed/ # Dados processados (versionados)
│ ├── dengue_consolidado_2019_2025.csv (30.633 registros)
│ ├── casos_dengue_bairros_2020_2025.csv (8.402 registros)
│ └── dados_integrados_dengue_clima.csv (157 semanas)
├── models/
│ └── modelo_dengue_emprel_producao.pkl
├── scripts/ # Pipeline de processamento
│ ├── 01_consolidar_dados_dengue.py
│ ├── 04_integracao_dados.py
│ ├── 05_treinar_modelo.py
│ │ ├── converter_codigos_bairros.py
│ ├── popular_mongodb_completo.py
│ └── script-main.py # Executa pipeline completo
├── outputs/ # Graficos e relatorios
├── .env # Variaveis de ambiente (nao versionado)
├── .gitignore
├── requirements.txt
└── README.md

## Requisitos

- Python 3.10+
- MongoDB (local ou Atlas)
- Bibliotecas listadas em `requirements.txt`

## Instalacao

```bash
git clone https://github.com/seu-usuario/projeto-dengue-recife.git
cd projeto-dengue-recife
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Configuracao

Crie um arquivo `.env` na raiz do projeto:

```env
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=dengue_recife
```

Para MongoDB Atlas:
```env
MONGODB_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/
DATABASE_NAME=dengue_recife
```

## Uso

### 1. Executar Pipeline Completo

```bash
python scripts/script-main.py
```

Este script executa automaticamente:
1. Consolidacao de dados de dengue
2. Integracao com dados climaticos
3. Conversao de codigos de bairros
4. Treinamento do modelo ML
5. Carga no MongoDB

### 2. Executar API

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse a documentacao interativa em `http://localhost:8000/docs`

## API Endpoints

### Informacoes Gerais

```http
GET /                        # Informacoes da API
GET /health                  # Status do sistema
GET /docs                    # Documentacao Swagger
```

### Casos de Dengue

```http
GET /api/casos
GET /api/casos?ano=2024
GET /api/casos?ano=2024&semana=20
```

**Exemplo de resposta:**
```json
{
  "total": 46,
  "dados": [
    {"ANO": 2024, "SEMANA": 1, "CASOS": 87, "TEMP_MEDIA_C": 27.5}
  ]
}
```

### Bairros

```http
GET /api/bairros                           # Lista todos os bairros
GET /api/casos/bairros                     # Casos de todos os bairros
GET /api/casos/bairros?bairro=Casa Amarela # Casos de um bairro especifico
GET /api/casos/bairros?ano=2024            # Casos por bairro em um ano
```

### Rankings e Totalizadores

```http
GET /api/bairros/ranking                   # Top 10 bairros
GET /api/bairros/ranking?ano=2024&limit=20 # Top 20 de 2024
GET /api/bairros/todos                     # Todos os 93 bairros com totais
GET /api/bairros/todos?ano=2024            # Totais por bairro em 2024
```

**Exemplo de resposta:**
```json
{
  "ranking": [
    {"bairro": "Casa Amarela", "casos": 1347},
    {"bairro": "Cajueiro", "casos": 972}
  ]
}
```

### Timeline e Analises

```http
GET /api/bairros/{bairro}/timeline         # Serie temporal de um bairro
GET /api/casos/bairros/por-ano?ano=2024    # Casos detalhados por bairro/ano
```

**Exemplo de resposta (timeline):**
```json
{
  "bairro": "Casa Amarela",
  "total_casos": 1347,
  "total_semanas": 156,
  "timeline": [
    {"ANO": 2020, "SEMANA": 1, "CASOS": 5},
    {"ANO": 2020, "SEMANA": 2, "CASOS": 8}
  ]
}
```

**Exemplo de resposta (por-ano):**
```json
{
  "ano": 2024,
  "total_casos": 4001,
  "total_bairros": 90,
  "bairros": [
    {
      "bairro": "Casa Amarela",
      "casos": 287,
      "semanas_com_casos": 48
    }
  ]
}
```

### Estatisticas

```http
GET /api/estatisticas/resumo               # Dashboard resumo geral
```

**Exemplo de resposta:**
```json
{
  "total_casos": 20947,
  "total_bairros": 93,
  "periodo": "2020-2025",
  "casos_por_ano": [
    {"ano": 2020, "casos": 3540},
    {"ano": 2021, "casos": 4053}
  ]
}
```

## Fontes de Dados

| Fonte | Tipo | Periodo | Registros |
|-------|------|---------|-----------|
| SINAN - Portal Dados Abertos Recife | Casos dengue | 2020-2025 | 30.633 |
| INMET | Clima (temp, umidade, precipitacao) | 2020-2025 | 35.064 |
| Portal Dados Abertos Recife | Mapeamento bairros (GeoJSON) | 2025 | 94 |

## Metodologia

### Feature Engineering

- Lags temporais: 1, 2, 3, 4 semanas
- Medias moveis: 2, 4, 8 semanas
- Variaveis climaticas: temperatura, precipitacao, umidade
- Features temporais: ano, semana epidemiologica

### Validacao

- Time Series Split com 3 folds
- Holdout set de 20% (80/20 split temporal)
- Metricas: MAE, RMSE, R2

### Modelo Selecionado

**Ridge Regression** (regressao linear regularizada)
- Alpha: 10.0
- MAE em validacao cruzada: 12.49 casos/dia
- MAE no conjunto de teste: 10.86 casos/dia
- R2 no conjunto de teste: 0.629
- Features: 16 variaveis (clima + lags + medias moveis)

**Comparacao com outros modelos:**
| Modelo | MAE (CV) | R2 (CV) |
|--------|----------|---------|
| Ridge Regression | 12.49 | 0.036 |
| XGBoost | 11.56 | -0.009 |
| Random Forest | 13.07 | -0.129 |

Ridge foi escolhido por ter melhor R2 sem overfitting.

## Stack Tecnologica

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| Backend | Python 3.10, FastAPI | Performance e integracao com Data Science |
| Processamento | Pandas, NumPy | Manipulacao eficiente de series temporais |
| ML | Scikit-learn, XGBoost | Modelos robustos para dados tabulares |
| Visualizacao | Matplotlib, Plotly | Graficos de alta qualidade |
| Banco de Dados | MongoDB | NoSQL flexivel para dados semi-estruturados |
| HTTP Client | Requests | Download automatizado de dados |

## Dados no MongoDB

### Collection: casos_dengue
- 157 documentos
- Campos: ANO, SEMANA, CASOS, TEMP_MEDIA_C, PRECIPITACAO_MM, UMIDADE_MEDIA
- Periodo: 2021-2025

### Collection: casos_por_bairro
- 8.402 documentos
- Campos: ANO, SEMANA, BAIRRO, CASOS
- Periodo: 2020-2025
- Bairros: 93 (oficiais da Prefeitura do Recife)

## Roadmap

### Fase 1: Fundacao e ETL (Concluida)
- Coleta automatizada de dados
- Limpeza e tratamento de valores nulos
- Analise exploratoria de dados
- Mapeamento oficial de bairros

### Fase 2: Inteligencia e Backend (Concluida)
- Treinamento e validacao de modelos
- Desenvolvimento da API FastAPI
- Integracao com MongoDB
- 10 endpoints REST funcionais

### Fase 3: Frontend e Deploy (Planejada)
- Dashboard interativo com graficos temporais
- Mapa de calor por bairro (GeoJSON)
- Integracao front-back
- Deploy automatizado com CI/CD

## Consideracoes de Seguranca

- Dados de saude utilizados sao publicos e agregados por regiao
- Sem informacoes pessoais identificaveis (PII)
- Rate limiting na API
- Conformidade com LGPD

## Licenca

MIT License

## Autores

Gabriel Ernandes, Bernardo Simões , Thayza Vitória, Raissa Vitória, Fabricio Estevam e Pedro Victor.

## Contato

Para duvidas ou sugestoes, abra uma issue no repositorio.

---

**Desenvolvido com dados publicos da Prefeitura do Recife e INMET**
