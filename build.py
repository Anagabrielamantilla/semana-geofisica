from pathlib import Path
import importlib.util
import re
import json
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent
SOURCE = Path('/Users/anagabriela/.codex/visualizations/2026/10/12/01a12df7-f398-77b3-b54a-3b3a4daf7082/semana-geofisica.html')
RENDER = Path('/Users/anagabriela/.codex/plugins/cache/openai-bundled/visualize/1.0.47/skills/visualize/scripts/render.py')
fragment = SOURCE.read_text()
# Shared visitors always see the published data, without browser-local overrides.
fragment = re.sub(r'<details>.*?</details>', '', fragment, flags=re.S)
fragment = fragment.replace("window.addEventListener('openai:set_globals',e=>{if(e.detail?.globals?.widgetState)apply(e.detail.globals.widgetState);});", '')
fragment = fragment.replace('apply(window.openai?.widgetState);', 'apply(null);')
fragment = fragment.replace('Base: notas del 9 de octubre · Fechas relativas confirmadas · Reserva de Eduardo Rosello unificada', 'Versión compartida · Actualizaciones automáticas · Horario de Colombia')
viewer = PROJECT / 'shared-view.html'
viewer.write_text(fragment)
spec = importlib.util.spec_from_file_location('visualize_render', RENDER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
document = module.render(viewer, title='Semana de la Geofísica · UIS 2026')
version = datetime.now(timezone.utc).isoformat()
document = document.replace('<meta charset="utf-8">', '<meta charset="utf-8"><meta name="geo-version" content="' + version + '">')
document = document.replace('connect-src blob: data:', "connect-src 'self' blob: data:")
document = document.replace("script-src 'unsafe-inline'", "script-src 'self' 'unsafe-inline'")
document = document.replace('<html lang="en"', '<html lang="es"')
document = document.replace('color-scheme:light dark;background:light-dark(rgb(255 255 255), rgb(24 24 24))', 'color-scheme:light;background:rgb(255 255 255)')
document = document.replace('</body>\n</html>', '<script src="refresh.js"></script>\n</body>\n</html>')
(PROJECT / 'dist' / 'index.html').write_text(document)
(PROJECT / 'dist' / 'version.json').write_text(json.dumps({'version': version}))
(PROJECT / 'dist' / '.nojekyll').touch()
print('Built shared dashboard in dist/')
