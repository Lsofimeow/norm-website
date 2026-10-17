# NORM website

Original English product website for an AI-assisted drone mission workspace,
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
- `site.config.json`: public domain, contact readiness, operator identity, release flag.
- `dist/`: the only directory intended to be served publicly.
- `.github/workflows/pages.yml`: build/check/deploy through GitHub Pages.

## Deployment

Use a dedicated website repository. Do not add the incoming handoff archive,
reference captures, project memos, private QA folder, or credentials to it.

The initial configuration is a preview: contact unverified, operator unknown,
`public_release: false`, and `noindex` pages. It can be deployed as an accurate
informational preview. The contact page clearly says the inbox is in preparation
and has no nonfunctional email button. Legal pages identify their preview status.
These limited missing inputs do not block the rest of the site from being shown.

After confirmation, update the privacy/site notes for the actual deployed
configuration, fill `operator_name`, set `email_verified` and `public_release` to
true, and rebuild. Complete browser QA before treating the artifact as accepted.

Set repository Settings → Pages → Source to GitHub Actions. Configure the custom
domain as `normautonomy.com` in GitHub Pages settings. The `CNAME` file is included
for branch-based hosting compatibility; it does **not** set the custom domain
when using Actions. Push the website source to `main` and inspect the deployment
result. Only `dist/` is uploaded by the workflow.

See `DEPLOYMENT.md` for DNS, canonical redirects, and the email routing plan.

## Verification limits

Static link, manifest, metadata, sitemap, SVG and leak checks can run offline.
Browser layout/interaction checks must be recorded separately. Product status
is project reported; building this website does not test the NORM application.
There is no public installer, demo endpoint, compatibility matrix or evidence
download in this artifact.
