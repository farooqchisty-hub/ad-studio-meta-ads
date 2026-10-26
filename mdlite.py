"""Small markdown to HTML used by the review pages."""
import html, re
e = html.escape


def md(text):
    """Small markdown to HTML: headings, tables, lists, code fences, paragraphs, bold, inline code."""
    out, lines, i = [], text.split('\n'), 0
    inl = lambda s: re.sub(r'`([^`]+)`', r'<code>\1</code>', re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', e(s)))
    while i < len(lines):
        l = lines[i]
        if l.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                j += 1
            out.append('<pre>' + e('\n'.join(lines[i + 1:j])) + '</pre>'); i = j + 1; continue
        if re.match(r'^#{1,4} ', l):
            n = min(len(l) - len(l.lstrip('#')) + 2, 5); out.append(f'<h{n}>{inl(l.lstrip("#").strip())}</h{n}>'); i += 1; continue
        if l.strip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            head = [c.strip() for c in l.strip().strip('|').split('|')]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip().startswith('|'):
                rows.append([c.strip() for c in lines[j].strip().strip('|').split('|')]); j += 1
            out.append('<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{inl(h)}</th>' for h in head) + '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join(f'<td>{inl(c)}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')
            i = j; continue
        if re.match(r'^\s*([-*]|\d+\.) ', l):
            tag = 'ol' if re.match(r'^\s*\d+\.', l) else 'ul'; items = []
            while i < len(lines) and re.match(r'^\s*([-*]|\d+\.) ', lines[i]):
                items.append(re.sub(r'^\s*([-*]|\d+\.) ', '', lines[i])); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inl(x)}</li>' for x in items) + f'</{tag}>'); continue
        if l.strip():
            para = [l]; i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|\s*([-*]|\d+\.) )', lines[i]):
                para.append(lines[i]); i += 1
            out.append('<p>' + inl(' '.join(para)) + '</p>'); continue
        i += 1
    return '\n'.join(out)
