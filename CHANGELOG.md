
Este proyecto sigue un versionado tipo SemVer (O.y.z mientras sea experimental).

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