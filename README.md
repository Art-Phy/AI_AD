## README.md

### AI Authorship Detector (Python)

Detector experimental para estimar si un texto fue generado por IA o por una persona.
El objetivo es construir un sistema **medible y calibrado**, con umbrales y modo conservador.

> Nota: la detección perfecta no existe; aquí buscamos **la mejor aproximación práctica** y bien documentada.

### Estado
- v0.0.0: estructura inicial del proyecto.

### Requisitos
- Python 3.10+ recomendado

### Desarrollo rápido
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest