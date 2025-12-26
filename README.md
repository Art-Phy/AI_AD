
### AI Authorship Detector

Detector experimental para estimar si un texto fue generado por IA o por una persona.

El sistema se basa en **heurísticas explicables**, no en modelos opacos,
y devuelve siempre una **estimación probabilística**, nunca certezas absolutas.

> Nota: la detección perfecta no existe; aquí buscamos **la mejor aproximación práctica** y bien documentada.
---
### Características

- Análisis de texto mediante métricas lingüísticas
- Salida en JSON
- CLI simple y portable
- Diseño modular y testeado
- Sin dependencias pesadas

### Estado
- v0.1.0: estructura inicial del proyecto.

### Requisitos
- Python 3.10+ recomendado

### Instalación (desarrollo)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
### Uso
```bash
python -m aidetect text archivo.txt
```
> [!WARNING]
> ##### Limitaciones
    - No existe detección perfecta de IA
    - Textos editados o híbridos son difíciles de clasificar
    - El resultado debe interpretarse como orientativo
