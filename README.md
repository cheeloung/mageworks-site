# mageworks-site

Public website for **MageWorks AI** (MageWorks AI Solutions), hosted on Cloudflare Pages.

- `main` = what's live on mageworks.ai
- Other branches get their own Cloudflare preview URL. Review there before merging.

## Structure

| Path | What it is |
|---|---|
| `public/` | Everything that gets published (Cloudflare build output directory) |
| `public/index.html` | Homepage ("Above the Clouds" design) |
| `public/privacy.html` | Privacy Notice (EN + BM), served at `/privacy`. **Generated: don't edit by hand** |
| `public/404.html` | Page-not-found |
| `public/_headers` | Security and caching headers |
| `public/assets/` | Self-hosted fonts (OFL), icons, link-preview image |
| `content/privacy/` | Source text of the Privacy Notice (EN and BM Markdown) |
| `tools/build_privacy.py` | Rebuilds `public/privacy.html` from `content/privacy/` |
| `docs/CLOUDFLARE-SETUP.md` | One-time Cloudflare, form, domain and email setup |

## Updating the Privacy Notice

1. Edit `content/privacy/privacy-notice-en.md` and `privacy-notice-ms.md` (keep them in step, and update "Last updated").
2. Run `python3 tools/build_privacy.py` (needs `pip install markdown`).
3. Update the form's hidden `privacy_notice_version` in `public/index.html` to the same date.

## Third parties used by the site

Cloudflare (hosting), Web3Forms (form delivery), hCaptcha (spam check). Fonts are self-hosted, so there are no Google requests. Keep the Privacy Notice in step if this list changes.

Only website files belong here. Secrets (API keys, tokens, `.env`) must never be committed. See `.gitignore`.
