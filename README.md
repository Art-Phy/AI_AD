![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![Tests](https://img.shields.io/badge/Tests-49_Passing-success)
![Version](https://img.shields.io/badge/Version-v1.1.0-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

### AI Authorship Detector

Detector experimental de autoría de texto para estimar si un contenido ha sido generado por una IA o escrito por una persona.

El sistema estable se basa actualmente en **heurísticas explicables** y devuelve siempre una **estimación probabilística**, nunca certezas absolutas.

La rama `develop` incorpora además un **baseline experimental de Machine Learning** destinado a investigar nuevas estrategias de clasificación antes de integrarlas en el detector principal.

Incluye:

- CLI para uso local
- API REST para integración
- Interfaz web ligera integrada
- Modos de decisión según tolerancia
- Autenticación mediante API Key y rate limiting
- Logging estructurado en JSON
- Endpoint de reportes descargables
- Controles de privacidad para reportes
- Pipeline experimental de Machine Learning
- Evaluación mediante métricas y validación cruzada

---

#### Características

- Análisis de texto mediante métricas lingüísticas explicables
- Score continuo (0–1)
- Modos de detección: `conservative`, `balanced`, `aggressive`
- Salida en JSON
- CLI simple y portable
- API REST con Swagger (`/docs`)
- API Keys y rate limiting por clave
- Request ID por petición (`X-Request-ID`)
- Logging estructurado en JSON
- Web UI integrada en FastAPI
- Reportes JSON con persistencia opcional
- Tests automatizados y releases versionadas
- Baseline experimental de Machine Learning basado en Logistic Regression
- Pipeline de entrenamiento con estandarización mediante `StandardScaler`
- División estratificada de datos de entrenamiento y test
- Evaluación mediante accuracy, precision, recall, F1 y matriz de confusión
- Validación cruzada estratificada mediante 5 folds

---

#### Estado

- **v1.1.0:** Primer baseline experimental de Machine Learning.
- El detector público continúa utilizando el sistema heurístico estable.
- El pipeline ML está funcional y validado, pero permanece en fase experimental.

---

#### Machine Learning Baseline

La rama `develop` incorpora el primer pipeline funcional de Machine Learning de AI Authorship Detector.

El objetivo actual no es sustituir inmediatamente al detector heurístico, sino disponer de una base reproducible para experimentar, medir resultados y comparar distintos enfoques.

El pipeline utiliza cinco características lingüísticas:

- `avg_sentence_length`
- `sentence_length_variance`
- `lexical_diversity`
- `punctuation_ratio`
- `max_word_frequency_ratio`

Flujo actual:

```text
Texto
  ↓
Extracción de features
  ↓
StandardScaler
  ↓
Logistic Regression
  ↓
Clasificación
```

El entrenamiento utiliza:

- `StandardScaler`
- `LogisticRegression`
- división `train/test` estratificada
- `random_state` fijo para reproducibilidad
- validación cruzada mediante `StratifiedKFold`

El dataset piloto actual contiene:

```text
60 muestras
├── 30 human
└── 30 ai

10 topics
└── 6 muestras por topic
```

Cada topic contiene tres textos humanos y tres textos generados por IA.

El dataset se utiliza actualmente como **baseline experimental y de validación del pipeline**, no como conjunto de datos suficiente para realizar afirmaciones generales sobre detección de contenido generado por IA.

##### Limitaciones actuales del baseline ML

El dataset piloto tiene varias limitaciones conocidas:

- Número reducido de muestras.
- Los textos humanos proceden actualmente de un único autor.
- Los textos AI proceden actualmente de un único generador.
- El modelo puede estar aprendiendo diferencias entre estilos concretos en lugar de patrones universales de autoría humana frente a IA.
- Las métricas obtenidas deben considerarse experimentales.
- El modelo todavía no se utiliza en producción ni forma parte de las respuestas de la API.

El siguiente trabajo sobre el baseline está orientado al análisis de errores, ampliación de diversidad del dataset y evaluación de nuevas features únicamente cuando exista evidencia que justifique su incorporación.

---

#### Requisitos

- Python **3.10+**

---

#### Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

---

#### Deployment

AI Authorship Detector puede desplegarse como un servicio persistente en sistemas Linux.

El proyecto incorpora un comando específico para ejecutar la API:

```bash
aidetect-api
```

Toda la configuración se realiza mediante variables de entorno, permitiendo separar completamente la configuración del código.

| Variable | Descripción | Valor por defecto |
|----------|-------------|------------------|
| `AIDETECT_API_HOST` | Dirección donde escucha la API | `127.0.0.1` |
| `AIDETECT_API_PORT` | Puerto de escucha | `8000` |
| `AIDETECT_API_KEYS` | API Keys permitidas | — |
| `AIDETECT_UI_MODE` | Habilita autenticación simplificada para la Web UI | `0` |
| `AIDETECT_LOG_LEVEL` | Nivel de logging | `INFO` |
| `AIDETECT_LOG_FILE` | Ruta del fichero de logs | Consola |
| `AIDETECT_REPORTS_DIR` | Directorio donde guardar reportes | No definido |

Ejemplo:

```bash
export AIDETECT_API_HOST=0.0.0.0
export AIDETECT_API_PORT=8003

export AIDETECT_API_KEYS=devkey
export AIDETECT_UI_MODE=1

aidetect-api
```

El proyecto ha sido validado ejecutándose como servicio **systemd** sobre Linux utilizando:

- entorno virtual independiente
- configuración mediante `EnvironmentFile`
- reinicio automático
- despliegue persistente tras reinicio del sistema

---

#### Uso CLI

```bash
aidetect-cli text archivo.txt

aidetect-cli text archivo.txt --pretty

aidetect-cli text archivo.txt --output resultado.json

aidetect-cli text archivo.txt --verbose

aidetect-cli text archivo.txt --mode conservative

aidetect-cli text archivo.txt --mode aggressive
```

También puede ejecutarse mediante:

```bash
python -m aidetect text archivo.txt
```

---

#### Modos de detección

El detector ofrece tres modos de operación.

| Modo | Descripción |
|------|-------------|
| `conservative` | Minimiza falsos positivos. Solo clasifica como IA con alta confianza. |
| `balanced` | Equilibrio entre precisión y cobertura (modo por defecto). |
| `aggressive` | Maximiza la detección de IA asumiendo un mayor riesgo de falsos positivos. |

> **Importante:** el *score* es estable y comparable; el modo únicamente modifica la interpretación del resultado.

---

#### Uso API

Arrancar la API:

```bash
AIDETECT_API_KEYS=devkey aidetect-api
```

También puede ejecutarse directamente con Uvicorn:

```bash
AIDETECT_API_KEYS=devkey uvicorn aidetect.api.app:app --reload
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

---

#### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Estado del servicio |
| GET | `/version` | Versión de ejecución |
| GET | `/v1/modes` | Lista de modos disponibles |
| POST | `/v1/analyze/text` | Análisis de texto |
| POST | `/v1/analyze/text/report` | Informe completo del análisis |
| GET | `/ui` | Interfaz web integrada |

---

#### Web UI integrada

La API incorpora una interfaz web ligera para usuarios no técnicos.

```text
http://127.0.0.1:8000/ui
```

Permite:

- Pegar texto
- Elegir modo
- Introducir la API Key
- Visualizar los resultados
- Copiar el JSON generado
- Descargar un informe JSON
- Decidir si incluir el texto completo en el informe

---

#### Autenticación

Los endpoints `/v1/*` requieren API Key.

---

#### UI Mode

Para facilitar el uso de la interfaz web durante el desarrollo existe un modo específico:

```bash
export AIDETECT_UI_MODE=1
export AIDETECT_API_KEYS=devkey

aidetect-api
```

---

#### Rate limiting

La API aplica **rate limiting** por API Key.

```bash
export AIDETECT_RATE_LIMIT_REQUESTS=60
export AIDETECT_RATE_LIMIT_WINDOW_SECONDS=60
```

---

#### Logging

La API genera logs estructurados en formato JSON.

```bash
export AIDETECT_LOG_LEVEL=INFO
```

Logs rotativos:

```bash
export AIDETECT_LOG_FILE="./logs/aidetect.log"
export AIDETECT_LOG_MAX_BYTES=1000000
export AIDETECT_LOG_BACKUP_COUNT=3
```

---

#### Reportes

```text
POST /v1/analyze/text/report
```

Devuelve un informe completo con:

- `generated_at`
- `request_id`
- `input`
- `result`
- `saved_to` (si se guarda en disco)

Guardar automáticamente los reportes:

```bash
export AIDETECT_REPORTS_DIR="./reports"
```

Por defecto el informe **no almacena el texto completo**, únicamente su longitud.

```json
{
  "input": {
    "mode": "balanced",
    "text_length": 22
  }
}
```

Si se desea incluir el texto completo:

```text
POST /v1/analyze/text/report?include_text=true
```

> La Web UI incluye un checkbox para activar esta opción.

---

#### Limitaciones

- No existe una detección perfecta de IA.
- Los textos editados o híbridos son especialmente difíciles de clasificar.
- El resultado debe interpretarse como una estimación orientativa.
- El uso de API Keys por query parameter está pensado únicamente para desarrollo local y la Web UI.
- En producción se recomienda utilizar siempre el header `X-API-Key`.
- Los textos híbridos tienden a clasificarse como **uncertain**.
- El baseline ML actual utiliza un dataset piloto pequeño y no debe interpretarse como un modelo listo para producción.
- El sistema ML todavía no forma parte de la CLI, API ni Web UI.

---

Este proyecto sigue versionado mediante **Semantic Versioning (SemVer)**. Durante la fase experimental utilizó la serie `0.y.z`.