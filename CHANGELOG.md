# Changelog

## 2026-11-06: Security and performance review fixes
- Performance: the hero animation pauses when it's off screen (it was redrawing constantly) and runs at about 20 fps; the mountain only rebuilds when the size actually changes.
- Privacy/security: hCaptcha now loads from hCaptcha directly (no web3forms.com script) and only when the visitor nears the form, so most page views contact no third party.
- Headers: Content-Security-Policy (only our own site, hCaptcha and Web3Forms allowed), HSTS, frame-ancestors 'none' / X-Frame-Options DENY.
- Removed an internal note from the page source.
- Fix: captcha box no longer grows on error (class name clash).

## 2026-11-06: Design changes on site-v1
- Hero lighting: warm sun glow from the top-left and a diagonal sky gradient; the mountain's left slopes catch warm light while the right side stays in shadow.
- Form: missing fields or captcha make the fields, captcha and Send button shake, with a red highlight.
- Send button: text centred with an arrow; while sending the arrow nudges, and on success the text slides out to the right and a green "Sent ✓" slides in.
- Link-preview image refreshed with the new lighting.
- Cast shadow: the mountain throws a soft lavender shadow across the cloud tops towards the bottom-right, away from the top-left sun. It fades into the dense cloud bank so there are no hard edges.

## 2026-11-06: Site v1 (branch `site-v1`)
- Homepage from the approved "Above the Clouds" concept: self-hosted fonts, SEO and link-preview tags, icons, WhatsApp buttons removed for now.
- Enquiry form via Web3Forms with hCaptcha spam check, notice line, optional marketing opt-in, and the notice version recorded with each submission. Web3Forms access key added (form "mageworks.ai enquiry form").
- Privacy Notice at `/privacy` (EN + BM) with defaults filled: address "to follow", registration "in progress", retention 12 months / 90 days / 7 years, deletion 3 working days / 30 days. Providers updated: Cloudflare, Web3Forms, hCaptcha added; Google Fonts removed.
- 404 page, security headers, robots.txt, sitemap.xml, Cloudflare setup guide.
