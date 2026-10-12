from pathlib import Path
import subprocess
import sys

PROJECT = Path(__file__).resolve().parent
BUNDLED_GIT = Path('/Users/anagabriela/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/git')
GIT = str(BUNDLED_GIT) if BUNDLED_GIT.exists() else 'git'

def git(*args, capture=False):
    result = subprocess.run([GIT, '-c', 'credential.helper=!gh auth git-credential',
        '-c', 'user.name=Ana Gabriela Mantilla',
        '-c', 'user.email=87718083+Anagabrielamantilla@users.noreply.github.com',
        *args], cwd=PROJECT, check=True, text=True,
        stdout=subprocess.PIPE if capture else None)
    return result.stdout.strip() if capture else None

subprocess.run([sys.executable, str(PROJECT / 'build.py')], check=True)
git('add', 'README.md', 'AGENTS.md', 'build.py', 'deploy.py', 'board-source.html', 'shared-view.html', 'dist')
if git('diff', '--cached', '--name-only', capture=True):
    git('commit', '-m', 'Update shared event dashboard')
git('push', 'origin', 'main')
git('fetch', 'origin', 'gh-pages')
tree = git('rev-parse', 'HEAD:dist', capture=True)
parent = git('rev-parse', 'FETCH_HEAD', capture=True)
commit = git('commit-tree', tree, '-p', parent, '-m', 'Deploy updated dashboard', capture=True)
git('push', 'origin', commit + ':refs/heads/gh-pages')
print('Deployment requested: https://anagabrielamantilla.github.io/semana-geofisica/')
