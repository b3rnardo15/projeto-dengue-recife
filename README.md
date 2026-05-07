# Sistema Inteligente de Predição de Surtos de Dengue

Plataforma analítica para previsão de picos epidemiológicos de dengue em Recife, utilizando correlação entre dados históricos de saúde e variáveis climáticas.

## Visão Geral

Este projeto foi desenvolvido para fornecer subsídios a órgãos de saúde pública na antecipação de ações de controle vetorial e alocação de recursos hospitalares, através de predições com antecedência de 4 a 8 semanas.

## Características Técnicas

- Pipeline completo de ETL para dados epidemiológicos e climáticos
- Feature engineering temporal com lags e médias móveis
- Modelo de regressão Ridge com validação temporal
- Métricas: MAE de 10.86 casos/dia e R² de 0.629

## Estrutura do Projeto

```
projeto-dengue-recife/
├── data/
│   ├── raw/                  # Dados brutos (não versionados)
│   └── processed/            # Dados processados
├── models/                   # Modelos treinados (.pkl)
├── scripts/                  # Pipeline de processamento
├── api/                      # FastAPI endpoints
├── outputs/                  # Gráficos e relatórios
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.9+
- Bibliotecas listadas em `requirements.txt`

## Instalação

```bash
git clone https://github.com/seu-usuario/projeto-dengue-recife.git
cd projeto-dengue-recife
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Uso

### 1. Coleta de Dados

```bash
python scripts/01_consolidar_dados_dengue.py
python scripts/02_baixar_dados_clima_inmet.py
```

### 2. Processamento

```bash
python scripts/03_analise_exploratoria.py
python scripts/04_integracao_dados.py
```

### 3. Treinamento do Modelo

```bash
python scripts/05_treinar_modelo.py
```

O modelo treinado será salvo em `models/modelo_dengue_emprel_producao.pkl`

### 4. Predição (API)

```bash
cd api
uvicorn main:app --reload
```

Acesse a documentação interativa em `http://localhost:8000/docs`

## Fontes de Dados

- Dados Epidemiológicos: Portal de Dados Abertos da Prefeitura de Recife
- Dados Climáticos: INMET (Instituto Nacional de Meteorologia)
- Dados Demográficos: IBGE

## Metodologia

### Feature Engineering

- Lags temporais: 7, 14, 21, 30 dias
- Médias móveis: 7, 14, 30 dias
- Variáveis climáticas: temperatura, precipitação, umidade
- Features temporais: mês, semana epidemiológica

### Validação

- Time Series Split com 3 folds
- Holdout set de 20% (80/20 split temporal)
- Métricas: MAE, RMSE, R²

### Modelo Selecionado

Ridge Regression (regressão linear regularizada)
- Alpha: 10.0
- MAE em validação cruzada: 12.49 casos/dia
- R² no conjunto de teste: 0.629

## Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| Backend | Python, FastAPI | Performance e integração com bibliotecas de Data Science |
| Processamento | Pandas, NumPy | Manipulação eficiente de séries temporais |
| ML | Scikit-learn | Modelos robustos para dados tabulares |
| Visualização | Matplotlib, Seaborn | Gráficos de alta qualidade |
| Banco de Dados | PostgreSQL | Armazenamento de dados históricos e logs de predição |

## Roadmap

### Fase 1: Fundação e ETL (Concluída)
- Coleta automatizada de dados
- Limpeza e tratamento de valores nulos
- Análise exploratória de dados

### Fase 2: Inteligência e Backend (Em Progresso)
- Treinamento e validação de modelos
- Desenvolvimento da API FastAPI
- Persistência de resultados

### Fase 3: Frontend e Deploy (Planejada)
- Dashboard Next.js com gráficos interativos
- Integração front-back
- Deploy automatizado com CI/CD

## Considerações de Segurança

- Dados de saúde utilizados são públicos e agregados por região
- Comunicação via HTTPS
- Rate limiting na API
- Conformidade com LGPD

## Licença

MIT License

## Autores

------ depois coloco nome de todoss

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.
