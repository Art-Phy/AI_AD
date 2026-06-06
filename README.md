![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![Tests](https://img.shields.io/badge/Tests-24_Passing-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

### AI Authorship Detector

Detector experimental de autoría de texto para estimar si un contenido ha sido generado por una IA o escrito por una persona.

El sistema se basa en **heurísticas explicables** y devuelve siempre una **estimación probabilística**, nunca certezas absolutas.

Incluye:

- CLI para uso local
- API REST para integración
- Interfaz Web ligera integrada
- Modos de decisión según tolerancia
- Autenticación por API Key + rate limiting
- Logging estructurado en JSON
- Endpoint de reportes descargables
- Controles de privacidad para reportes

---

#### Características

- Análisis de texto mediante métricas lingüísticas explicables
- Score continuo (0–1)
- Modos de detección: `conservative`, `balanced`, `aggressive`
- Salida en JSON
- CLI simple y portable
- API REST con Swagger (`/docs`)
- API keys + rate limiting por clave
- Request ID por petición (`X-Request-ID`)
- Logging estructurado en JSON
- Web UI integrada en FastAPI
- Reportes JSON con persistencia opcional
- Tests automatizados y releases versionados
- Sin dependencias pesadas de ML

---

#### Estado

- **v1.0.0:** First Stable Release

#### Requisitos

- Python **3.10+**

#### Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

---

#### Uso CLI
```
aidetect-cli text archivo.txt
aidetect-cli text archivo.txt --pretty
aidetect-cli text archivo.txt --output resultado.json
aidetect-cli text archivo.txt --verbose
aidetect-cli text archivo.txt --mode conservative
aidetect-cli text archivo.txt --mode aggressive
```
También se puede usar `python -m aidetect text archivo.txt`

---

#### Modos de detección

El detector ofrece tres modos de operación:

| Modo | Descripción |
|----|----|
| `conservative` | Minimiza falsos positivos. Solo clasifica como IA con alta confianza. |
| `balanced` | Equilibrio entre precisión y cobertura (modo por defecto). |
| `aggressive` | Maximiza detección de IA, asumiendo mayor riesgo de falsos positivos. |

**Importante:** el *score* es estable y comparable; el modo solo cambia la interpretación del resultado.

---

#### Uso API
- Ejecuta servidor `AIDETECT_API_KEYS=devkey aidetect-api`
- Se puede arrancar directamente desde **Uvicorn** `AIDETECT_API_KEYS=devkey uvicorn aidetect.api.app:app --reload`
- Documentación `http://127.0.0.1:8000/docs`

#### Endpoints
| Método | Endpoint | Descripción |
|----------------------|----------------------|----------------------|
| GET | /health | Estado del servicio |
| GET | /version | Versión de ejecución |
| GET | /v1/modes | Lista de modos disponibles |
| POST | /v1/analyze/text | Análisis de texto |
| POST | /v1/analyze/text/report | Informe completo del análisis |
| GET | /ui | Interfaz integrada |

---

#### Web UI integrada
La API incluye una interfaz web ligera para usuarios no técnicos.

```http://127.0.0.1:8000/ui````

* Pegar texto
* Elegir modo
* Introducir API key
* Ver resultados de forma visual
* Copiar el JSON resultante
* Descargar un informe JSON con metadatos
* Elegir si se incluye o no el texto completo en el informe

#### Autenticación
Los endpoints /v1/*requieren API key.

#### UI Mode
Para facilitar el uso de la interfaz web en desarrollo local, existe un modo UI.
```
export AIDETECT_UI_MODE=1
export AIDETECT_API_KEYS=devkey
aidetect-api
```

---

#### Rate limiting
La API aplica limiting por API key
```
export AIDETECT_RATE_LIMIT_REQUESTS=60
export AIDETECT_RATE_LIMIT_WINDOW_SECONDS=60
```

#### Logging
La API genera logs estructurados en **JSON**
```export AIDETECT_LOG_LEVEL=INFO```

Logs a ficheros rotaticvos
```
export AIDETECT_LOG_FILE="./logs/aidetect.log"
export AIDETECT_LOG_MAX_BYTES=1000000
export AIDETECT_LOG_BACKUP_COUNT=3
```
---

#### Reportes
```POST /v1/analyze/text/report```

Devuelve un informe completo con metadatos:
* generated_at
* request_id
* input
* result
* saved_to si se guarda en disco

Para guardar los reportes automáticamente en disco:
```export AIDETECT_REPORTS_DIR="./reports"```

Por defecto, los informes **no guardan el texto completo**, sólo su longitud:
```
{
  "input": {
    "mode": "balanced",
    "text_length": 22
  }
}
```
Si necesitas incluir texto completo
```POST /v1/analyze/text/report?include_text=true```

> ###### La web UI incluye un checkbox para activar esta opción.

---

> [!WARNING]
> ##### Limitaciones
    - No existe detección perfecta de IA
    - Textos editados o híbridos son difíciles de clasificar
    - El resultado debe interpretarse como orientativo
    - El uso de API keys por query param está pensado únicamente para desarrollo local y UI sencilla
    - Para producción se recomienda usar siempre el header `X-API-Keyu`
    - Textos híbridos tienden a clasificarse como **uncertain**
