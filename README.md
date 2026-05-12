# Sistema Inteligente de Predição de Surtos de Dengue

Plataforma analítica para previsão de picos epidemiológicos de dengue em Recife, utilizando correlação entre dados históricos de saúde e variáveis climáticas.

## Visão Geral

Este projeto foi desenvolvido para fornecer subsídios a órgãos de saúde pública na antecipação de ações de controle vetorial e alocação de recursos hospitalares, através de predições com antecedência de 4 a 8 semanas.

## Características Técnicas

- Pipeline completo de ETL para dados epidemiológicos e climáticos
- Feature engineering temporal com lags e médias móveis
- Modelo de regressão Ridge com validação temporal
- Métricas: MAE de 10.86 casos/dia e R² de 0.629
- API REST com FastAPI e MongoDB Atlas

## Estrutura do Projeto

```
projeto-dengue-recife/
├── api/                      # API FastAPI
│   ├── routers/
│   │   ├── historico.py     # Endpoints de consulta histórica
│   │   └── predict.py       # Endpoints de predição
│   ├── database.py          # Configuração MongoDB
│   ├── main.py              # Aplicação principal
│   └── models.py            # Schemas Pydantic
├── data/
│   ├── raw/                 # Dados brutos (não versionados)
│   └── processed/           # Dados processados
├── models/                  # Modelos treinados (.pkl)
├── notebooks/               # Análises exploratórias
├── scripts/                 # Pipeline de processamento
│   ├── 01_processar_casos_dengue.py
│   ├── 02_processar_clima_inmet.py
│   ├── 03_integrar_dados.py
│   ├── 04_treinar_modelo.py
│   └── 05_inserir_historico_mongodb.py
├── outputs/                 # Gráficos e relatórios
├── .env                     # Variáveis de ambiente (não versionado)
├── .gitignore
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.10+
- MongoDB Atlas (ou instância local)
- Bibliotecas listadas em `requirements.txt`

## Instalação

```bash
git clone https://github.com/seu-usuario/projeto-dengue-recife.git
cd projeto-dengue-recife
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/dengue_recife
DATABASE_NAME=dengue_recife
```

## Uso

### 1. Pipeline de Dados

```bash
python scripts/01_processar_casos_dengue.py
python scripts/02_processar_clima_inmet.py
python scripts/03_integrar_dados.py
```

### 2. Treinamento do Modelo

```bash
python scripts/04_treinar_modelo.py
```

O modelo treinado será salvo em `models/modelo_dengue_emprel_producao.pkl`

### 3. Carga de Dados Históricos

```bash
python scripts/05_inserir_historico_mongodb.py
```

### 4. Executar API

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse a documentação interativa em `http://localhost:8000/docs`

## API Endpoints

### Health Check
```http
GET /health
```

### Fazer Predição
```http
POST /api/v1/predict
Content-Type: application/json

{
  "precipitacao_mm": 25.5,
  "temp_media_c": 27.3,
  "umidade_media": 75.0,
  "ano": 2026,
  "semana": 20
}
```

### Consultar Histórico
```http
GET /api/v1/historico?ano=2025&semana=1
```

### Listar Predições
```http
GET /api/v1/predicoes?limite=10
```

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
- MAE no conjunto de teste: 10.86 casos/dia
- R² no conjunto de teste: 0.629

## Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| Backend | Python, FastAPI | Performance e integração com bibliotecas de Data Science |
| Processamento | Pandas, NumPy | Manipulação eficiente de séries temporais |
| ML | Scikit-learn | Modelos robustos para dados tabulares |
| Visualização | Matplotlib, Seaborn | Gráficos de alta qualidade |
| Banco de Dados | MongoDB Atlas | Armazenamento NoSQL escalável e flexível |

## Roadmap

### Fase 1: Fundação e ETL (Concluída)
- Coleta automatizada de dados
- Limpeza e tratamento de valores nulos
- Análise exploratória de dados

### Fase 2: Inteligência e Backend (Concluída)
- Treinamento e validação de modelos
- Desenvolvimento da API FastAPI
- Integração com MongoDB Atlas
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

------ depois coloco nome de todos

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.