
const btn = document.getElementById('btn');
const out = document.getElementById('output');
const summary = document.getElementById('summary');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');

function show(el, yes) {
  el.hidden = !yes;
}

function fmt(n) {
  return typeof n === 'number' ? n.toFixed(3) : n;
}

function nowIso() {
  return new Date().toISOString();
}

function downloadJson(filename, obj) {
  const blob = new Blob([JSON.stringify(obj, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

let lastSuccessful = null; // guardamos último análisis para exportar

btn.addEventListener('click', async () => {
  const text = document.getElementById('text').value;
  const mode = document.getElementById('mode').value;
  const apiKey = document.getElementById('apiKey').value;

  show(summary, true);
  show(out, true);
  show(copyBtn, false);
  show(downloadBtn, false);
  lastSuccessful = null;

  summary.textContent = 'Analizando...';
  out.textContent = '';
  btn.classList.add('loading');

  try {
    const url = `/v1/analyze/text?api_key=${encodeURIComponent(apiKey)}`;

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
      body: JSON.stringify({ text, mode })
    });

    const requestId = res.headers.get('X-Request-ID') || null;

    let data = null;
    try {
      data = await res.json();
    } catch {
      data = { detail: 'Respuesta no JSON del servidor' };
    }

    if (!res.ok) {
      summary.textContent = `Error ${res.status}: ${data.detail ?? 'Request failed'}`;
      out.textContent = JSON.stringify(data, null, 2);
      return;
    }

    const label = data.label ?? 'unknown';
    const score = fmt(data.score);
    const usedMode = data.details?.mode ?? mode;

    summary.textContent = `Resultado: ${label.toUpperCase()}  |  score=${score}  |  mode=${usedMode}`;
    out.textContent = JSON.stringify(data, null, 2);

    // Preparamos un "informe" exportable
    lastSuccessful = {
      generated_at: nowIso(),
      request_id: requestId,
      input: {
        mode: usedMode,
        text_length: (text || '').length,
        // No guardamos el texto completo por defecto (privacidad).
        // Si quieres incluirlo, lo añadimos luego como opción.
      },
      result: data
    };

    show(copyBtn, true);
    copyBtn.onclick = async () => {
      await navigator.clipboard.writeText(out.textContent);
      copyBtn.textContent = 'Copiado ✅';
      setTimeout(() => (copyBtn.textContent = 'Copiar resultado'), 1200);
    };

    show(downloadBtn, true);
    downloadBtn.onclick = () => {
      if (!lastSuccessful) return;
      const safeTs = lastSuccessful.generated_at.replace(/[:.]/g, '-');
      const filename = `aidetect-report-${safeTs}.json`;
      downloadJson(filename, lastSuccessful);
    };
  } catch (err) {
    summary.textContent = 'Error de conexión';
    out.textContent = String(err);
  } finally {
    btn.classList.remove('loading');
  }
});

