
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

function downloadJson(filename, obj) {
  const blob = new Blob(
    [JSON.stringify(obj, null, 2)],
    { type: 'application/json' }
  );

  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = filename;

  document.body.appendChild(a);
  a.click();
  a.remove();

  URL.revokeObjectURL(url);
}

let lastSuccessful = null;

btn.addEventListener('click', async () => {

  const text = document.getElementById('text').value;
  const mode = document.getElementById('mode').value;
  const apiKey = document.getElementById('apiKey').value;
  const includeText = document.getElementById('includeText').checked;

  show(summary, true);
  show(out, true);
  show(copyBtn, false);
  show(downloadBtn, false);

  lastSuccessful = null;

  summary.textContent = 'Analizando...';
  out.textContent = '';

  btn.classList.add('loading');

  try {

    const url =
      `/v1/analyze/text/report` +
      `?api_key=${encodeURIComponent(apiKey)}` +
      `&include_text=${includeText}`;

    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      },
      body: JSON.stringify({ text, mode })
    });

    let data;

    try {
      data = await res.json();
    } catch {
      data = { detail: 'Respuesta no JSON del servidor' };
    }

    if (!res.ok) {
      summary.textContent =
        `Error ${res.status}: ${data.detail ?? 'Request failed'}`;

      out.textContent = JSON.stringify(data, null, 2);
      return;
    }

    const result = data.result ?? {};
    const details = result.details ?? {};

    const label = result.label ?? 'unknown';
    const score = fmt(result.score);
    const usedMode = data.input?.mode ?? details.mode ?? mode;

    let extra = '';

    if (data.saved_to) {
      extra = ` | saved_to=${data.saved_to}`;
    }

    summary.textContent =
      `Resultado: ${label.toUpperCase()} | score=${score} | mode=${usedMode}${extra}`;

    out.textContent = JSON.stringify(data, null, 2);

    lastSuccessful = data;

    show(copyBtn, true);
    copyBtn.onclick = async () => {

      await navigator.clipboard.writeText(out.textContent);

      copyBtn.textContent = 'Copiado ✅';

      setTimeout(() => {
        copyBtn.textContent = 'Copiar resultado';
      }, 1200);
    };

    show(downloadBtn, true);

    downloadBtn.onclick = () => {

      if (!lastSuccessful) return;

      const ts =
        (lastSuccessful.generated_at || new Date().toISOString())
          .replace(/[:.]/g, '-');

      downloadJson(
        `aidetect-report-${ts}.json`,
        lastSuccessful
      );
    };

  } catch (err) {

    summary.textContent = 'Error de conexión';
    out.textContent = String(err);

  } finally {

    btn.classList.remove('loading');

  }
});
