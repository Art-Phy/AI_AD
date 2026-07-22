![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![Tests](https://img.shields.io/badge/Tests-24_Passing-success)
![Version](https://img.shields.io/badge/Version-v1.0.2-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

### AI Authorship Detector

Detector experimental de autoría de texto para estimar si un contenido ha sido generado por una IA o escrito por una persona.

El sistema se basa en **heurísticas explicables** y devuelve siempre una **estimación probabilística**, nunca certezas absolutas.

Incluye:

- CLI para uso local
- API REST para integración
- Interfaz web ligera integrada
- Modos de decisión según tolerancia
- Autenticación mediante API Key y rate limiting
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
- API Keys y rate limiting por clave
- Request ID por petición (`X-Request-ID`)
- Logging estructurado en JSON
- Web UI integrada en FastAPI
- Reportes JSON con persistencia opcional
- Tests automatizados y releases versionadas
- Sin dependencias pesadas de Machine Learning

---

#### Estado

- **v1.0.2:** Versión estable preparada para despliegue.

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

```
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

```
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

```
POST /v1/analyze/text/report
```

Devuelve un informe completo con:

- generated_at
- request_id
- input
- result
- saved_to (si se guarda en disco)

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

```
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

---

Este proyecto sigue versionado **Semantic Versioning (SemVer)**. Durante la fase experimental utilizó la serie `0.y.z`.
