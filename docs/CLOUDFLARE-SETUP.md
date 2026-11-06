# Cloudflare setup for mageworks.ai

One-time setup. Takes about 20 minutes. Domain DNS is already on Cloudflare.

## 1. Connect this repository to Cloudflare Pages

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** tab → **Connect to Git** (it may be called "Import an existing Git repository").
2. Choose **GitHub**, authorise Cloudflare, and select **cheeloung/mageworks-site** only.
3. Build settings:
   - **Production branch:** `main`
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `public`
4. Save and deploy.

`main` only has the README until the first version is approved and merged, so the very first production deploy may be empty. That's expected.

Every other branch (e.g. `site-v1`) gets its own **preview URL** like `https://site-v1.mageworks.pages.dev`. Find it under the project → **Deployments**. Review there before anything is merged to `main`.

## 2. Web3Forms (enquiry form)

1. Go to **web3forms.com**, enter the email address where enquiries should arrive, and click to create an access key. The key is emailed to you.
2. Send the key to Claude. It's safe to be public, so it goes straight into the page.
3. In the Web3Forms dashboard, open the form's settings and turn on **hCaptcha** spam protection.

Until the key is added, the form politely tells visitors to email info@mageworks.ai instead.

## 3. Custom domain (after the first version is merged to `main`)

1. Pages project → **Custom domains** → **Set up a custom domain** → `mageworks.ai`. Cloudflare adds the DNS record automatically.
2. Repeat for `www.mageworks.ai`.
3. Optional: a **Redirect Rule** so `www.mageworks.ai` goes to `mageworks.ai`.
4. Check `https://mageworks.ai` and `https://mageworks.ai/privacy` load in a private browser window.

## 4. Email Routing (info@mageworks.ai)

1. Cloudflare → your domain → **Email** → **Email Routing** → enable it, and accept the DNS records it adds.
2. **Routing rules** → create `info@mageworks.ai` → forward to your inbox, then verify the destination address from the email Cloudflare sends.
3. Send a test email to info@mageworks.ai.

This receives only. To *send* as info@mageworks.ai, add a mail provider later (e.g. Google Workspace or Zoho).

## 5. Meta app review (WhatsApp Enquiry Assistant)

Only once `https://mageworks.ai/privacy` loads publicly:

- **Privacy Policy URL:** `https://mageworks.ai/privacy`
- **User data deletion instructions URL:** `https://mageworks.ai/privacy#delete-your-data`
