
### AI Authorship Detector

Detector experimental de autoría de texto para estimar si un contenido ha sido
generado por una IA o escrito por una persona.

El sistema se basa en **heurísticas explicables** y devuelve siempre una
**estimación probabilística**, nunca certezas absolutas.


Incluye:
 - CLI para uso local
 - API REST para integración
 - Modos de decisión según tolerancia
 - Autenticación por API Key + rate limiting (SaaS-ready)

---

### Características

- Análisis de texto mediante métricas lingüísticas explicables
- Score continuo (0–1)
- Modos de detección según tolerancia: `conservative` `balanced` `aggresive`
- Salida en JSON
- CLI simple y portable
- API REST con Swagger (`/docs`)
- API keys + rate limiting por clave
- Tests y releases versionados
- Sin dependencias pesadas de ML

### Estado
- v0.4.0: API REST ready

### Requisitos
- Python 3.10+ recomendado

### Modos de detección

El detector ofrece tres modos de operación:

| Modo | Descripción |
|----|----|
| `conservative` | Minimiza falsos positivos. Solo clasifica como IA con alta confianza. |
| `balanced` | Equilibrio entre precisión y cobertura (modo por defecto). |
| `aggressive` | Maximiza detección de IA, asumiendo mayor riesgo de falsos positivos. |

**Importante:** el *score* es estable y comparable; el modo solo cambia la interpretación.

---

### Instalación (desarrollo)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
### Uso(CLI)
```bash
python -m aidetect text archivo.txt
python -m aidetect text archivo.txt --pretty
python -m aidetect text archivo.txt --output resultado.json
python -m aidetect text archivo.txt --verbose
python -m aidetect text archivo.txt --mode conservative
python -m aidetect text archivo.txt --mode aggressive

```
### Uso(API)
```bash
uvicorn aidetect.api.app:app --reload
```
- Documentación interactiva
    - Swagger UI: http://127.0.0.1:8000/docs
- Endpoints
    - `GET /health` -> estado del servicio
    - `GET /v1/mode` -> lista de modos disponibles
    - `GET /v1/analyze/text` -> análisis de texto

### UI Mode (desarrollo local)
Para facilitar la creación de una interfaz web ligera en entorno local, existe un **modo UI** opcional.
Cuando `AIDETECT_UI_MODE=1`, la API acepta la API key también por query param (`?api_key=...`) además del header `X-API-Key`.

>###### ⚠️ Importante: fuera de UI mode (`AIDETECT_UI_MODE=0`), el parámetro `?api_key=...` **se ignora** y solo se acepta `X-API-Key`.

```
export AIDETECT_UI_MODE=1
export AIDETECT_API_KEYS=devkey
uvicorn aidetect.api.app:app --reload
```

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
