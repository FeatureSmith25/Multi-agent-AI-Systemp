const form = document.querySelector('#research-form');
const topicInput = document.querySelector('#topic');
const submitButton = document.querySelector('#submit-button');
const charCount = document.querySelector('#char-count');
const pipelineStatus = document.querySelector('#pipeline-status');
const steps = [...document.querySelectorAll('.agent-step')];
const emptyState = document.querySelector('#empty-state');
const resultState = document.querySelector('#result-state');
const errorState = document.querySelector('#error-state');
const reportContent = document.querySelector('#report-content');
const downloadButton = document.querySelector('#download-button');
let latestReport = '';

topicInput.addEventListener('input', () => { charCount.textContent = `${topicInput.value.length} / 500`; });
document.querySelectorAll('.topic-chip').forEach(chip => chip.addEventListener('click', () => {
  topicInput.value = chip.textContent.trim();
  topicInput.dispatchEvent(new Event('input'));
  topicInput.focus();
}));

function setStep(name, state, preview = '') {
  const item = steps.find(step => step.dataset.step === name);
  if (!item) return;
  item.classList.remove('running', 'done');
  if (state !== 'waiting') item.classList.add(state);
  const label = item.querySelector('.step-state');
  label.textContent = state === 'running' ? 'Working…' : state === 'done' ? 'Complete' : 'Waiting';
  if (preview) item.title = preview;
}

function setBusy(busy) {
  submitButton.disabled = busy;
  submitButton.querySelector('span:first-child').textContent = busy ? 'Researching…' : 'Start research';
  const complete = !busy && steps.length > 0 && steps.every(step => step.classList.contains('done'));
  pipelineStatus.className = `status-pill${busy ? ' running' : complete ? ' done' : ''}`;
  pipelineStatus.innerHTML = `<span class="status-dot"></span> ${busy ? 'IN PROGRESS' : complete ? 'COMPLETE' : 'READY'}`;
}

function resetView() {
  emptyState.classList.add('hidden');
  resultState.classList.add('hidden');
  errorState.classList.add('hidden');
  steps.forEach(step => setStep(step.dataset.step, 'waiting'));
}

function showError(message) {
  setBusy(false);
  errorState.classList.remove('hidden');
  document.querySelector('#error-message').textContent = message;
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  const topic = topicInput.value.trim();
  if (topic.length < 3) return;
  resetView();
  setBusy(true);
  try {
    const response = await fetch('/api/research', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
      body: JSON.stringify({ topic }),
    });
    if (!response.ok || !response.body) throw new Error(`The server returned ${response.status}. Check that the API is running and try again.`);
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const blocks = buffer.split('\n\n');
      buffer = blocks.pop() || '';
      for (const block of blocks) {
        const eventName = block.match(/^event: (.+)$/m)?.[1];
        const dataLine = block.match(/^data: (.+)$/m)?.[1];
        if (!eventName || !dataLine) continue;
        const data = JSON.parse(dataLine);
        if (eventName === 'stage') setStep(data.step, data.status, data.preview || '');
        if (eventName === 'error') throw new Error(data.message);
        if (eventName === 'complete') renderResult(data);
      }
    }
  } catch (error) {
    showError(error.message || 'Something went wrong while running the research pipeline.');
  } finally {
    setBusy(false);
  }
});

function renderResult(data) {
  latestReport = data.report || '';
  document.querySelector('#result-topic').textContent = data.topic;
  const rendered = window.marked ? marked.parse(latestReport) : `<pre>${escapeHtml(latestReport)}</pre>`;
  reportContent.innerHTML = window.DOMPurify ? DOMPurify.sanitize(rendered) : rendered;
  document.querySelector('#search-content').textContent = data.search || '';
  document.querySelector('#reader-content').textContent = data.reader || '';
  emptyState.classList.add('hidden');
  errorState.classList.add('hidden');
  resultState.classList.remove('hidden');
  downloadButton.disabled = !latestReport;
  pipelineStatus.className = 'status-pill done';
  pipelineStatus.innerHTML = '<span class="status-dot"></span> COMPLETE';
}

function escapeHtml(value) { return value.replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]); }

document.querySelector('#sources-toggle').addEventListener('click', () => {
  const content = document.querySelector('#sources-content');
  const opening = content.classList.contains('hidden');
  content.classList.toggle('hidden', !opening);
  document.querySelector('#sources-chevron').textContent = opening ? '−' : '＋';
});

downloadButton.addEventListener('click', () => {
  if (!latestReport) return;
  const blob = new Blob([latestReport], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `evidence_brief_${new Date().toISOString().slice(0, 10)}.md`;
  link.click();
  URL.revokeObjectURL(url);
});
