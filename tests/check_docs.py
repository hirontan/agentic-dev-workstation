from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
errors = []
for source in root.rglob('*.md'):
    text = source.read_text()
    if text.count('```') % 2:
        errors.append(f'Unbalanced code fences: {source}')
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if '://' in target or target.startswith('#'):
            continue
        path = target.split('#')[0]
        if path and not (source.parent / path).exists():
            errors.append(f'Broken link: {source.relative_to(root)} -> {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: Markdown file links and code fences')
