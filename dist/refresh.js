(() => {
  let currentVersion = document.querySelector('meta[name="geo-version"]')?.content;
  let checking = false;
  async function checkVersion() {
    if (checking) return;
    checking = true;
    try {
      const response = await fetch('version.json?check=' + Date.now(), { cache: 'no-store' });
      if (!response.ok) return;
      const data = await response.json();
      if (typeof data.version !== 'string') return;
      if (currentVersion && currentVersion !== data.version) location.reload();
      currentVersion = data.version;
    } catch {
      // Keep the current board visible while offline.
    } finally {
      checking = false;
    }
  }
  checkVersion();
  setInterval(checkVersion, 60000);
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) checkVersion();
  });
})();
