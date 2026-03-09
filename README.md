
## AI Authorship Detector

Detector experimental de autoría de texto para estimar si un contenido ha sido generado por una IA o escrito por una persona.

El sistema se basa en **heurísticas explicables** y devuelve siempre una **estimación probabilística**, nunca certezas absolutas.

Incluye:

- CLI para uso local
- API REST para integración
- Interfaz Web ligera integrada
- Modos de decisión según tolerancia
- Autenticación por API Key + rate limiting (SaaS-ready)

---

### Características

- Análisis de texto mediante métricas lingüísticas explicables
- Score continuo (0–1)
- Modos de detección según tolerancia: `conservative`, `balanced`, `aggressive`
- Salida en JSON
- CLI simple y portable
- API REST con Swagger (`/docs`)
- API keys + rate limiting por clave
- Logging estructurado en JSON
- Endpoint de reportes descargables
- Tests automatizados y releases versionados
- Sin dependencias pesadas de ML

---

### Estado

- **v0.9.0:** Privacy-aware reporting (`include_text`)

---

### Requisitos

- Python **3.10+** recomendado

---

### Modos de detección

El detector ofrece tres modos de operación:

| Modo | Descripción |
|----|----|
| `conservative` | Minimiza falsos positivos. Solo clasifica como IA con alta confianza. |
| `balanced` | Equilibrio entre precisión y cobertura (modo por defecto). |
| `aggressive` | Maximiza detección de IA, asumiendo mayor riesgo de falsos positivos. |

**Importante:** el *score* es estable y comparable; el modo solo cambia la interpretación del resultado.

---

### Instalación (desarrollo)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

```
#### Uso(CLI)
```bash
python -m aidetect text archivo.txt
python -m aidetect text archivo.txt --pretty
python -m aidetect text archivo.txt --output resultado.json
python -m aidetect text archivo.txt --verbose
python -m aidetect text archivo.txt --mode conservative
python -m aidetect text archivo.txt --mode aggressive

```
#### Uso(API)
```bash
uvicorn aidetect.api.app:app --reload
```
- Documentación interactiva
    - Swagger UI: http://127.0.0.1:8000/docs
- Endpoints
    - `GET /health` -> estado del servicio
    - `GET /version` -> devuelve la versión en ejecución
    - `GET /v1/modes` -> lista de modos disponibles
    - `POST /v1/analyze/text` -> análisis de texto
    - `POST /v1/analyz/text/report` -> genera informe completo

#### Web UI integrada
La API incluye una interfaz web ligera para uso de usuarios no técnicos.

#### Accesso(con la API arrancada)
```
http://127.0.0.1:8000/ui
```
 - Pegar texto
 - Elegir modo
 - Introducir API key
 - Ver resultados de forma visual
 - Copiar el JSON resultante
 - Descargar un **informe JSON** con metadatos (timestamp, request_id, modo, etc.)


#### UI Mode (desarrollo local)
Para facilitar la creación de una interfaz web ligera en entorno local, existe un **modo UI**.
Cuando `AIDETECT_UI_MODE=1`, la API acepta la API key también por query param (`?api_key=...`) además del header `X-API-Key`.

```
export AIDETECT_UI_MODE=1
export AIDETECT_API_KEYS=devkey
uvicorn aidetect.api.app:app --reload
```
>##### ⚠️ Importante: fuera de UI mode (`AIDETECT_UI_MODE=0`), el parámetro `?api_key=...` **se ignora** y solo se acepta `X-API-Key`.

#### Logging
La API genera logs estructurados en formato JSON, pensados para depuración y trazabilidad.
- Configuración:
```
export AIDETECT_LOG_LEVEL=INFO
```

#### Endpoint de report (API + UI)

Además del análisis estándar, existe un endpoint que devuelve un **informe** con metadatos:

- `POST /v1/analyze/text/report`

Incluye:
- `generated_at` (timestamp)
- `request_id`
- `input` (mode, text_length)
- `result` (score, label, details)
- `saved_to` (solo si se guarda en disco)

Ejemplo (UI mode):

```bash
curl -s -X POST "http://127.0.0.1:8000/v1/analyze/text/report?api_key=devkey" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola mundo. Hola mundo","mode":"balanced"}'

### Observaciones
- Falsos positivos muy bajos (prioridad del proyecto)
- Falsos negativos posibles en textos IA bien redactados
- Textos híbridos tienden a `uncertain`

> [!WARNING]
> ##### Limitaciones
    - No existe detección perfecta de IA
    - Textos editados o híbridos son difíciles de clasificar
    - El resultado debe interpretarse como orientativo
    - El uso de API keys por query param está pensado únicamente para desarrollo local y UI sencilla
    - Para producción se recomienda usar siempre el header `X-API-Keyu`
