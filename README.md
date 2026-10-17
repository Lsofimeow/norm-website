# NORM website

English and Chinese product website for an AI-assisted drone mission workspace,
focused on fixed-wing waypoint missions. Plain HTML, CSS and JavaScript; no runtime
dependencies, analytics, forms, payment, model API, or device connection.

## Local use

Build the site, then open `dist/index.html` directly. The downloadable preview package includes the prebuilt files. All regular pages use explicit relative HTML
links. The standalone 404 includes a separate local-home link and has inline
styling so it also works when GitHub serves it at an arbitrary missing URL.

Rebuild with Python 3.9+:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check src/js/site.js
```

The browser needs none of these tools. Python and Node are build/check tools only.
The prebuilt sharing image is retained in `src/assets/og/` and copied during build.

## Source layout

- `scripts/build.py`: shared templates, page content, original SVG illustrations.
- `src/css/site.css`: responsive styles at desktop, tablet, and mobile breakpoints.
- `src/js/site.js`: mobile navigation and illustrated workflow controls.
- `scripts/localize.py` and `src/i18n/zh-CN.json`: build-time Chinese translations,
  including metadata, accessible labels, diagrams, and same-page language links.
- `src/assets/product/`: six original application captures supplied by the owner.
- `site.config.json`: public domain, contact readiness, operator identity, release flag.
- `dist/`: the only directory intended to be served publicly.
- `.github/workflows/pages.yml`: build/check/deploy through GitHub Pages.

## Deployment

Use a dedicated website repository. Do not add the incoming handoff archive,
reference captures, project memos, private QA folder, or credentials to it.

The configuration remains a preview: operator unknown, `public_release: false`,
and `noindex` pages. The contact address is published at the owner's request.
Its destination verification and routing are enabled; end-to-end email receipt
has not been tested. `contact_enabled` and `email_receipt_tested` record these
different states. Legal pages identify their preview status.

After confirmation, update the privacy/site notes for the actual deployed
configuration, fill `operator_name`, set `email_verified` and `public_release` to
true, and rebuild. The isolated design revision has completed Chromium browser QA; see `BROWSER_ACCEPTANCE.json` for its exact tested source revision and scope.

Set repository Settings → Pages → Source to GitHub Actions. Configure the custom
domain as `normautonomy.com` in GitHub Pages settings. The `CNAME` file is included
for branch-based hosting compatibility; it does **not** set the custom domain
when using Actions. Push the website source to `main` and inspect the deployment
result. Only `dist/` is uploaded by the workflow.

See `DEPLOYMENT.md` for DNS, canonical redirects, and the email routing plan.

The visual revision lives on `design/uforce-reference-v2`. The production branch
and deployment workflow are unchanged. Open `dist/zh/index.html` for Chinese;
the language switch preserves the current page. See `VISUAL_REDESIGN.md` for the
revision scope and actual verification limits.

## Verification limits

Static link, manifest, metadata, sitemap, SVG and leak checks can run offline.
Chromium layout and interaction checks are recorded in `BROWSER_ACCEPTANCE.json`; `qa/capture.mjs` and the isolated visual QA workflow reproduce them. Product status
is project reported; building this website does not test the NORM application.
There is no public installer, demo endpoint, compatibility matrix or evidence
download in this artifact.
