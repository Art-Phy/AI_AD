
const btn = document.getElementById('btn');
const out = document.getElementById('output');
const summary = document.getElementById('summary');
const copyBtn = document.getElementById('copyBtn');

function show(el, yes) {
  el.hidden = !yes;
}

function fmt(n) {
  return typeof n === 'number' ? n.toFixed(3) : n;
}

btn.addEventListener('click', async () => {
  const text = document.getElementById('text').value;
  const mode = document.getElementById('mode').value;
  const apiKey = document.getElementById('apiKey').value;

  show(summary, true);
  show(out, true);
  show(copyBtn, false);

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

    // Resumen “humano”
    const label = data.label ?? 'unknown';
    const score = fmt(data.score);
    const usedMode = data.details?.mode ?? mode;

    summary.textContent = `Resultado: ${label.toUpperCase()}  |  score=${score}  |  mode=${usedMode}`;
    out.textContent = JSON.stringify(data, null, 2);

    show(copyBtn, true);
    copyBtn.onclick = async () => {
      await navigator.clipboard.writeText(out.textContent);
      copyBtn.textContent = 'Copiado ✅';
      setTimeout(() => (copyBtn.textContent = 'Copiar resultado'), 1200);
    };
  } catch (err) {
    summary.textContent = 'Error de conexión';
    out.textContent = String(err);
  } finally {
    btn.classList.remove('loading');
  }
});
