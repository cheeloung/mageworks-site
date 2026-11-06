import re, sys, html
import markdown

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "content", "privacy") + "/"
OUT = os.path.join(ROOT, "public", "privacy.html")


def slug(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"^\d+\.\s*", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def convert(path, prefix, table_label):
    md = open(path, encoding="utf-8").read()
    md = re.sub(r"<!--.*?-->\s*", "", md, flags=re.S)
    body = markdown.markdown(md, extensions=["tables", "nl2br", "sane_lists"])
    # move standalone anchors onto the following h2
    body = re.sub(r'(?:<p>)?<a id="([^"]+)"></a>(?:</p>)?\s*<h2>', r'<h2 id="\1">', body)
    toc = []

    def add_id(m):
        attrs, text = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs or "")
        hid = idm.group(1) if idm else f"{prefix}-{slug(text)}"
        toc.append((hid, re.sub(r"<[^>]+>", "", text)))
        return f'<h2 id="{hid}">{text}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", add_id, body)
    # first h1 + "Last updated" paragraph -> header
    body = re.sub(r"<h1>(.*?)</h1>\s*<p>(.*?)</p>",
                  r'<header class="doc-head"><h1>\1</h1><p class="updated">\2</p></header>', body, count=1, flags=re.S)
    # responsive tables
    body = body.replace("<table>", f'<div class="table-wrap" role="region" aria-label="{table_label}" tabindex="0"><table>')
    body = body.replace("</table>", "</table></div>")
    # external links open normally; mark them for screen readers is unnecessary. Highlight placeholders.
    def ph(m):
        return f'<span class="ph">{m.group(0)}</span>'
    parts = re.split(r"(<[^>]+>)", body)
    for i, p in enumerate(parts):
        if not p.startswith("<"):
            parts[i] = re.sub(r"\[[^\[\]]+\]", ph, p)
    body = "".join(parts)
    # short-version list as callout
    body = body.replace(f'<h2 id="{toc[0][0]}">', f'<section class="summary" aria-labelledby="{toc[0][0]}"><h2 id="{toc[0][0]}">', 1)
    body = re.sub(r'(<section class="summary".*?</ul>)', r"\1</section>", body, count=1, flags=re.S)
    return body, toc


def toc_html(toc, label, prefix):
    items = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc)
    return f'<details class="toc"><summary>{label}</summary><ol>{items}</ol></details>'


en, en_toc = convert(SRC + "privacy-notice-en.md", "en", "Table, scroll sideways on small screens")
ms, ms_toc = convert(SRC + "privacy-notice-ms.md", "bm", "Jadual, tatal ke sisi pada skrin kecil")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Privacy Notice | MageWorks AI</title>
<meta name="description" content="How MageWorks AI Solutions handles personal data from website visitors, enquiries and our WhatsApp AI Enquiry Assistant, and how to delete your data.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://mageworks.ai/privacy">
<link rel="alternate" hreflang="en" href="https://mageworks.ai/privacy">
<link rel="alternate" hreflang="ms" href="https://mageworks.ai/privacy#bm">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<style>
:root {{
  --cream: #fbf6ef;
  --ink: #2d2533;
  --muted: #5d5266;
  --accent: #c7655a;
  --accent-ink: #a64b41;
  --line: #e6ddd3;
  --card: #fffaf4;
  --ph: #f6e1d6;
  --serif: "Fraunces", Georgia, "Times New Roman", serif;
  --sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}}
*, *::before, *::after {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
body {{
  margin: 0; background: var(--cream); color: var(--ink);
  font: 400 1.0625rem/1.7 var(--sans);
}}
a {{ color: var(--accent-ink); text-underline-offset: 3px; text-decoration-thickness: 1px; }}
a:hover {{ color: var(--ink); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 3px; }}
.skip {{ position: absolute; left: -9999px; top: 0; }}
.skip:focus {{ left: 16px; top: 12px; background: var(--ink); color: var(--cream); padding: 8px 14px; z-index: 10; }}

.topbar {{ border-bottom: 1px solid var(--line); background: var(--cream); position: sticky; top: 0; z-index: 5; }}
.topbar-inner {{ max-width: 760px; margin: 0 auto; padding: 14px 24px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
.brand {{ display: inline-flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none; font: 600 1.125rem/1 var(--serif); letter-spacing: -0.01em; }}
.brand svg {{ color: var(--accent); flex: none; }}
.lang {{ display: flex; gap: 4px; font-size: 0.875rem; font-weight: 500; }}
.lang a {{ white-space: nowrap; text-decoration: none; color: var(--muted); padding: 6px 10px; border-radius: 999px; border: 1px solid transparent; }}
.lang a:hover {{ color: var(--ink); border-color: var(--line); }}
.lang a.on {{ color: var(--ink); border-color: var(--ink); }}
body:has(#bm:target) .lang a.on, body:has(#bm :target) .lang a.on {{ color: var(--muted); border-color: transparent; }}
body:has(#bm:target) .lang a[href="#bm"], body:has(#bm :target) .lang a[href="#bm"] {{ color: var(--ink); border-color: var(--ink); }}

main {{ max-width: 760px; margin: 0 auto; padding: 56px 24px 80px; }}
.notice {{ display: block; scroll-margin-top: 100px; }}
.short {{ display: none; }}
@media (max-width: 480px) {{ .long {{ display: none; }} .short {{ display: inline; }} }}
#bm {{ display: none; }}
#bm:target, #bm:has(:target) {{ display: block; }}
#bm:target ~ #en {{ display: none; }}
body:has(#bm :target) #en {{ display: none; }}

.doc-head {{ margin-bottom: 32px; }}
h1 {{ font: 600 clamp(2.25rem, 6vw, 3.25rem)/1.1 var(--serif); letter-spacing: -0.02em; margin: 0 0 12px; }}
.updated {{ color: var(--muted); font-size: 0.9375rem; margin: 0; }}
h2 {{ font: 600 1.625rem/1.25 var(--serif); letter-spacing: -0.01em; margin: 56px 0 16px; padding-top: 24px; border-top: 1px solid var(--line); scroll-margin-top: 80px; }}
h3 {{ font: 600 1.125rem/1.4 var(--sans); margin: 28px 0 8px; }}
p, ul, ol {{ margin: 0 0 16px; }}
ul, ol {{ padding-left: 1.3em; }}
li {{ margin-bottom: 8px; }}
li::marker {{ color: var(--accent); }}
strong {{ font-weight: 600; }}

.summary {{ background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: 14px; padding: 4px 28px 12px; margin: 32px 0 8px; }}
.summary h2 {{ border-top: 0; margin-top: 20px; padding-top: 0; font-size: 1.375rem; }}
.summary li:first-child {{ font-size: 1.0625rem; }}

h2#delete-your-data, h2#padam-data-anda {{ color: var(--ink); }}
h2#delete-your-data::before, h2#padam-data-anda::before {{ content: ""; display: block; width: 40px; height: 3px; background: var(--accent); margin-bottom: 16px; border-radius: 2px; }}

.toc {{ border: 1px solid var(--line); border-radius: 12px; padding: 12px 20px; margin: 24px 0 28px; background: transparent; }}
.toc summary {{ cursor: pointer; font-weight: 600; color: var(--ink); }}
.toc ol {{ margin: 12px 0 4px; columns: 2 240px; column-gap: 32px; font-size: 0.9375rem; }}
.toc li {{ break-inside: avoid; margin-bottom: 6px; }}
.toc a {{ color: var(--muted); text-decoration: none; }}
.toc a:hover {{ color: var(--ink); text-decoration: underline; }}

.table-wrap {{ overflow-x: auto; margin: 0 0 20px; border: 1px solid var(--line); border-radius: 12px; background: var(--card); }}
table {{ border-collapse: collapse; width: 100%; min-width: 600px; font-size: 0.9375rem; line-height: 1.55; }}
th, td {{ text-align: left; vertical-align: top; padding: 12px 16px; border-bottom: 1px solid var(--line); }}
th {{ font-weight: 600; background: #f5ede3; }}
tr:last-child td {{ border-bottom: 0; }}

.ph {{ background: var(--ph); color: var(--ink); border-radius: 4px; padding: 0 4px; font-size: 0.92em; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}

.site-foot {{ border-top: 1px solid var(--line); }}
.site-foot-inner {{ max-width: 760px; margin: 0 auto; padding: 24px; color: var(--muted); font-size: 0.875rem; display: flex; flex-wrap: wrap; gap: 8px 24px; justify-content: space-between; }}
.site-foot a {{ color: var(--muted); }}

@media (max-width: 600px) {{
  body {{ font-size: 1rem; }}
  .topbar-inner {{ padding: 12px 16px; }}
  main {{ padding: 36px 16px 64px; }}
  .summary {{ padding: 2px 18px 8px; }}
  h2 {{ margin-top: 44px; }}
  .site-foot-inner {{ padding: 20px 16px; }}
}}
@media print {{
  .topbar {{ position: static; }}
  .lang, .toc, .skip {{ display: none; }}
  #bm {{ display: block; break-before: page; }}
  #bm:target ~ #en {{ display: block; }}
}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="/" aria-label="MageWorks AI home">
      <svg viewBox="0 0 104 40" width="44" height="17" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"><path d="M2 38 L13 4 L24 26 L35 4 L46 38"/><path d="M58 2 L69 36 L80 14 L91 36 L102 2"/></g></svg>
      <span>mageworks.ai</span>
    </a>
    <nav class="lang" aria-label="Language / Bahasa">
      <a class="on" href="#en" hreflang="en" lang="en" aria-label="English"><span class="long">English</span><span class="short" aria-hidden="true">EN</span></a>
      <a href="#bm" hreflang="ms" lang="ms" aria-label="Bahasa Malaysia"><span class="long">Bahasa Malaysia</span><span class="short" aria-hidden="true">BM</span></a>
    </nav>
  </div>
</header>

<main id="main">
<article id="bm" class="notice" lang="ms" aria-label="Notis Privasi (Bahasa Malaysia)">
{ms.replace('</header>', '</header>' + toc_html(ms_toc, 'Kandungan', 'bm'), 1)}
</article>

<article id="en" class="notice" lang="en" aria-label="Privacy Notice (English)">
{en.replace('</header>', '</header>' + toc_html(en_toc, 'On this page', 'en'), 1)}
</article>
</main>

<footer class="site-foot">
  <div class="site-foot-inner">
    <span>&copy; 2026 MageWorks AI Solutions</span>
    <span><a href="mailto:info@mageworks.ai">info@mageworks.ai</a> &middot; <a href="#en" lang="en">Privacy Notice</a> &middot; <a href="#bm" lang="ms">Notis Privasi</a></span>
  </div>
</footer>
</body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(page)
print("ok", len(page), [t for t in en_toc][:3], ms_toc[-5:])
