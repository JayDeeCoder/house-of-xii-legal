"""Builds privacy.html, terms.html and support.html from the app's Legal.swift so the web copy always matches the app.
Run: python3 gen.py ~/house-of-xii-ios/HouseOfXII/Legal.swift"""
import re, html, sys

src = open(sys.argv[1]).read()
contact = 'xiistudios@xiimajiqstudios.com'
vals = {'legalName': 'XII Studios', 'dba': 'XII Majiq Studios', 'contact': contact, 'Legal.contact': contact,
        'Legal.privacyURL': 'https://jaydeecoder.github.io/house-of-xii-legal/privacy'}
vals['entity'] = f"{vals['legalName']}, doing business as {vals['dba']}"
version = re.search(r'version = "([^"]+)"', src).group(1)


def interp(s):
    s = s.replace('\\"', '"')
    return re.sub(r'\\\(([\w.]+)\)', lambda m: vals[m.group(1)], s)


def sections(name):
    block = re.search(r'static let ' + name + r': \[Section\] = \[(.*?)\n    \]\n', src, re.S).group(1)
    out = []
    for m in re.finditer(r'Section\(title: "((?:[^"\\]|\\.)*)", body: \[(.*?)\]\)', block, re.S):
        paras = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2))
        out.append((interp(m.group(1)), [interp(p) for p in paras]))
    return out


marks = interp(re.search(r'static let marks = "((?:[^"\\]|\\.)*)"', src).group(1))
CSS = """<style>:root{--bg:#0b0b0c;--fg:#ece7dd;--dim:#a39d92;--gold:#c9a45c}
@media (prefers-color-scheme: light){:root{--bg:#f6f3ee;--fg:#141414;--dim:#55524c;--gold:#8a6a2a}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif}
main{max-width:720px;margin:0 auto;padding:40px 16px 80px}h1{font-size:40px;letter-spacing:.02em;margin:.2em 0}
h2{font-size:18px;text-transform:uppercase;letter-spacing:.06em;margin-top:2em}p{color:var(--dim)}a{color:var(--gold)}
.eb{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}nav a{margin-right:16px;font-size:14px}
footer{margin-top:3em;font-size:12px;color:var(--dim)}</style>"""


def page(title, h1, intro, secs):
    body = ''.join(f"<h2>{html.escape(t)}</h2>" + ''.join(f"<p>{html.escape(p)}</p>" for p in ps) for t, ps in secs)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>{CSS}</head>
<body><main><nav><a href="./privacy">Privacy</a><a href="./terms">House terms</a><a href="./support">Support</a></nav>
<p class="eb">House of XII / updated {version}</p><h1>{h1}</h1>{intro}{body}
<footer><p>{html.escape(marks)}</p><p>{html.escape(vals['entity'])}. Questions: <a href="mailto:{contact}">{contact}</a></p></footer></main></body></html>
"""


intro = f"<p>This policy covers the XII app for iPhone (House of XII), run by {html.escape(vals['entity'])}.</p>"
open('privacy.html', 'w').write(page('XII Privacy Policy', 'Privacy', intro, sections('privacy')))
open('terms.html', 'w').write(page('XII House Terms', 'House terms', '', sections('terms')))
support = [
    ('Get help', [f"Email {contact} with what happened and your member number if you have one. The house answers within 3 business days."]),
    ('Your member key', ["Keys are issued by XII after a seat is approved. Lost or changed key: email the house from the address you applied with."]),
    ('Delete your data', ["In the app, open the House tab and tap Delete my account and data. To remove your application from the house inbox, email the house."]),
]
open('support.html', 'w').write(page('XII Support', 'Support', '', support))
open('index.html', 'w').write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=./privacy"><title>XII Legal</title><a href="./privacy">Privacy</a>\n')
print(version, len(sections('privacy')), 'privacy sections,', len(sections('terms')), 'terms sections')
