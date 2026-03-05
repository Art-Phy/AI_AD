
Este proyecto sigue un versionado tipo SemVer (O.y.z mientras sea experimental).

### v0.8.0 - 05.03.2026

#### Added
- Logging estructurado en JSON (una línea por evento) para trazabilidad y observabilidad.
- Configuración por variables de entorno para nivel de log y fichero rotativo.

#### Environment
- `AIDETECT_LOG_LEVEL` (default: `INFO`)
- `AIDETECT_LOG_FILE` (opcional): ruta del fichero de logs (si no se define, solo consola)
- `AIDETECT_LOG_MAX_BYTES` (default: `1000000`)
- `AIDETECT_LOG_BACKUP_COUNT` (default: `3`)

---

### v0.7.0 - 27.02.2026

#### Added
- Nuevo endpoint `POST /v1/analyze/text/report` que devuelve un informe completo (report) con metadatos.
- Persistencia opcional de reportes en disco mediante `AIDETECT_REPORTS_DIR`.
- La Web UI ahora consume el endpoint de report y permite descargar el informe tal cual lo devuelve la API.

#### Environment
- `AIDETECT_REPORTS_DIR` (opcional): ruta donde guardar reportes en JSON.

---

### v0.6.0 - 18.02.2026

#### Added
- `GET /version` para exponer la versión del servicio.
- Middleware de `request_id`:
  - Genera `X-Request-ID` en cada respuesta (o conserva el que envíe el cliente).
- Logging básico por request (método, path, status, ms, request_id).
- Web UI: exportar informe en JSON descargable desde la interfaz.

---

### v0.5.0 - 10.02.2026

#### Added
- Web UI integrada en FastAPI (`GET /ui`) para uso por usuarios no técnicos.
- Servido de assets estáticos (`/static/app.js`).
- Mejoras de UX: resumen del resultado y botón para copiar JSON.

#### Notes
- La API continúa protegida por API key y rate limiting. La UI es una capa ligera sobre `/v1/analyze/text`.

---

### v0.4.2 - 02.02.2026

#### Fixed
- La API key por query param (`?api_key=...`) solo se acepta cuando `AIDETECT_UI_MODE=1`.
- En modo normal (`AIDETECT_UI_MODE=0`), la autenticación se realiza únicamente mediante el header `X-API-Key`.

---

### v0.4.1 - 31.01.2026

#### Added
- Modo de autenticación amigable para UI local (`UI mode`).
- Posibilidad de pasar la API key por query param (`?api_key=...`) **solo** cuando `AIDETECT_UI_MODE=1`.

#### Changed
- La detección de `UI mode` ahora se evalúa en runtime para facilitar tests y configuración dinámica.

#### Security
- El uso de API key por query param está **deshabilitado por defecto**.
- Los endpoints `/v1/*` siguen requiriendo API key obligatoria salvo en modo explícito de UI local.

---

### v0.4.0 - 25.01.2026

#### Added
- Autenticación por API key para endpoints `/v1/*`.
- Healthcheck público en `/health`.
- Rate limiting en memoria por API key.
- Tests para auth y rate limiting (401/429).

#### Changed
- Configuración de rate limiting leída desde entorno de forma configurable para tests y despliegue.

#### Fixed
- Corrección de nombres de variables de entorno para API keys.

---

### v0.3.0 - 18.01.2026

#### Added
- API REST (FastAPI) para análisis de texto.
- Documentación automática vía Swager (/docs).
- Endpoint /v1/analyze/text con soporte de mode.
- Endpoint /v1/modes para consultar modos disponibles.
- Endpoint /health para healthcheck.
- Test de API usando TestClient (Starlette) + httpx.

#### Changed
- README ampliado con sección de API

---

### v0.2.0 - 31.12.2025

#### Added
- Modos de detección configurables (`conservative`, `balanced`, `aggressive`).
- Separación clara entre score y política de clasificación.
- Inclusión del modo activo en la salida de resultados.

#### Changed
- Interpretación del score desacoplada del cálculo de métricas.
- CLI ampliado con opción `--mode`.

#### Fixed
- Paso correcto de configuración desde CLI al core del detector.

---

### v0.1.0 - 26.12.2025

#### Added
- Detector de autoría de textos basado en heurísticas.
- CLI funcional con opciones de salida.
- Métricas lingüisticas explicables.
- Configuración desacoplada de umbrales.

#### Changed
- Arquitectura modular del análisis de texto.

#### Fixed
- [x] Configuración correcta de imports y ejecución como paquete.

---
### v0.0.0 - 17.12.2025
- Estructura inicial del proyecto.
- Añadidos README, LICENSE, CHANGELOG, requirements y configuración base.
- Paquete base aidetect y carpeta de tests.