
### AI Authorship Detector

Detector experimental de autoría de texto para estimar si un contenido ha sido
generado por una IA o escrito por una persona.

El sistema se basa en **heurísticas explicables** y devuelve siempre una
**estimación probabilística**, nunca certezas absolutas.

El objetivo del proyecto es ofrecer una **señal configurable y responsable**,
adecuada para distintos contextos de riesgo.

---
### Características

- Análisis de texto mediante métricas lingüísticas explicables
- Score continuo (0–1)
- Modos de detección según tolerancia al riesgo
- Salida en JSON
- CLI simple y portable
- Diseño modular, testeado y evaluable
- Sin dependencias pesadas

### Estado
- v0.2.0: estructura inicial del proyecto.

### Requisitos
- Python 3.10+ recomendado

### Modos de detección

El detector ofrece tres modos de operación:

| Modo | Descripción |
|----|----|
| `conservative` | Minimiza falsos positivos. Solo clasifica como IA con alta confianza. |
| `balanced` | Equilibrio entre precisión y cobertura (modo por defecto). |
| `aggressive` | Maximiza detección de IA, asumiendo mayor riesgo de falsos positivos. |

El **score es siempre el mismo**; solo cambia la interpretación.

---

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
python -m aidetect text archivo.txt --pretty
python -m aidetect text archivo.txt --output resultado.json
python -m aidetect text archivo.txt --verbose
python -m aidetect text archivo.txt --mode conservative
python -m aidetect text archivo.txt --mode aggressive

```
> [!WARNING]
> ##### Limitaciones
    - No existe detección perfecta de IA
    - Textos editados o híbridos son difíciles de clasificar
    - El resultado debe interpretarse como orientativo
