"""Extract only translated text and attributes from the generated static pages."""
import hashlib
import json
import re
from html.parser import HTMLParser

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
ATTRIBUTES = ('alt', 'aria-label', 'title', 'content', 'href')


class PageStrings(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.lines = [0] + [m.end() for m in re.finditer('\n', html)]
        self.nodes = []
        self.stack = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        if self.stack and self.stack[-1][2].get('class') == 'faq-answer-content':
            if tag != 'br':
                raise ValueError('Expected plain text and line breaks in FAQ answer')
            return
        line, column = self.getpos()
        node = (tag, self.lines[line - 1] + column + 1 + len(tag), dict(attrs), [])
        self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if self.stack and data.strip():
            self.stack[-1][3].append(data)


def build_messages(pages):
    files = ('kousei.html', 'index-en.html', 'index-jp.html')
    codes = ('zh-CN', 'en', 'ja')
    parsed = [PageStrings(pages[f]).nodes for f in files]
    inserts = [[] for _ in files]
    bundles = [[] for _ in files]
    schema = []
    for nodes in zip(*parsed, strict=True):
        tags, positions, attributes, texts = zip(*nodes)
        if len(set(tags)) != 1:
            raise ValueError(f'Locale markup differs near {tags}')
        keys = []
        if attributes[0].get('class') == 'faq-answer-content':
            fields = [('lines', ['\n'.join(parts) for parts in texts])]
        else:
            fields = [(str(i), v) for i, v in enumerate(zip(*texts, strict=True))]
        fields.extend((attr, [a.get(attr) for a in attributes]) for attr in ATTRIBUTES)
        for field, values in fields:
            if len(set(values)) == 1:
                continue
            if None in values:
                raise ValueError(f'Missing {field} on {tags[0]}')
            keys.append(field)
            for bundle, value in zip(bundles, values):
                bundle.append(value)
        if keys:
            schema.append((tags[0], keys))
            for edits, pos in zip(inserts, positions):
                edits.append((pos, ' data-msg="' + ' '.join(keys) + '"'))

    def compact(obj):
        return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

    version = hashlib.sha256(compact([schema, bundles]).encode()).hexdigest()[:12]
    for name, code, edits, bundle in zip(files, codes, inserts, bundles):
        page = pages[name]
        for pos, attr in reversed(edits):
            page = page[:pos] + attr + page[pos:]
        pages[name] = page.replace('<html ', f'<html data-msg-version="{version}" ', 1)
        pages[f'assets/locales/{code}.js'] = (
            'document.currentScript.messages=' + compact([version, code, bundle]) + ';\n')
