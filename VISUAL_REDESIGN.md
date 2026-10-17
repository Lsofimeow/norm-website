# NORM visual revision — 2026-10-17

## Review state

- Repository: `Lsofimeow/norm-website`; isolated branch: `design/uforce-reference-v2`.
- Baseline: `3765a453ab6152c86e28e70fc873ff930a3ffabe`.
- Browser-tested source: `2200d2db4352c6edc08c58e9033069aea5716d6e`.
- [Actual Chromium acceptance run](https://github.com/Lsofimeow/norm-website/actions/runs/39079829697): **PASS — 292 checks, 60 screenshots**.
- All 12 original English routes retained; 12 corresponding Chinese routes added under `/zh/`, plus a new bilingual download page (26 pages total).
- Production branch, Pages deployment workflow, CNAME and domain configuration remain unchanged. This revision has not been deployed.

## What changed and why

The original home and Platform pages were captured at 1440, 768 and 390 pixels
alongside the revised pages. Their left-aligned headline, abstract route diagram
and relatively compact media treatment were compared with the original UFORCE
home/C2 screenshots, rendered HTML and engineering records at those same widths.

Home and Platform now use a centered large headline over application imagery,
wide product captures, alternating pale/dark sections, large vertical image-led
entries, and a large NORM footer. They keep editable text and components. Shared
navigation, spacing, buttons and responsive rules carry through the other routes.

The six owner-supplied NORM screenshots are used unchanged. Image dialogs support
Escape and return focus to the opener. Captions identify disconnected, empty,
expired or warning states; those images are not presented as completed-flight
evidence. The existing interactive mission workflow remains functional.

English and Chinese use static routes and an editable translation dictionary.
Language switches preserve the page. Metadata, accessible labels and conceptual
diagrams are translated. Product screenshots remain in their original English.
The copy keeps the fixed-wing mission focus, packaged Windows preview and
incomplete real-aircraft execution acceptance. No specialist-foundry repositioning
or unsupported compatibility or performance claim was introduced.

The owner’s supplied product story is distributed across the homepage: a mission
starting with a sentence, scattered information, bringing preparation together,
retaining original requirements, preview scope, and the closing invitation.
All six supplied paragraphs are preserved in Chinese, with a natural English
version. Availability and limitations are also shown near downloads and on the
product page. In particular, the preview is not intended for real flights,
unattended operation, or production use. Eighteen content-presence checks passed.

`hello@normautonomy.com` appears on the contact page, home/product contact areas
and shared footer. Existing configuration records destination verification and
routing as enabled. This revision does not recheck or change email infrastructure;
end-to-end receipt is still NOT_RUN.

The owner's follow-up also adds a bilingual download page, navigation and home/
product download sections. They point to the fixed public GitHub Release page:
https://github.com/Lsofimeow/norm-website/releases/tag/windows-preview
The owner uploaded `NORM_Preview_1.0.0.zip` (660,493,462 bytes). The download
page now links directly to that file and separately to the fixed release page.
Anonymous HTTP HEAD checks the public download response and content length.
The complete 630 MiB package was not downloaded, audited or executed. The
separate release-preparation workflow maintains this requested public location;
it does not deploy the website. Upload directions are in
`distribution/UPLOAD_GUIDE.md`.

## Browser review and fixes

The first completed run produced 36 actual screenshots and 218 passing checks.
Visual inspection then found missing spaces at mobile line-break boundaries and
a Platform hero button that reopened its own page. Spaces were restored and the
button now goes to the workspace section. Chinese font fallbacks were improved.
A second screenshot review found an orphaned final character in the mobile
Chinese product headline, and a later review found the same issue in a story heading. The sentences were shortened without reducing type size.
The final run includes regression checks for all three issues.

The local managed preview could not start (`bwrap` mount permission failure).
Browser acceptance was therefore completed in an isolated GitHub Actions job
using Chromium 151.0.7922.34 on Linux, DPR 1, reduced motion, and Noto CJK fonts.
The job builds the exact baseline and candidate and serves them on localhost;
it has read-only repository permissions and no deployment step.

## Reference parameters and remaining visual differences

| Item | Captured reference | NORM implementation |
| --- | --- | --- |
| Desktop container | 1296 px at a 1440 px viewport | 1296 px maximum; 72 px side margins |
| Hero type | 72 px desktop, 44 px mobile | 72/44 px English; 64/40 px Chinese |
| Major spacing | About 120 px desktop, 60 px mobile | 110/60 px; adjusted to NORM content |
| Main media | Video and product imagery | Real NORM application stills |
| Product entrances | Vertical large-image sequence | Three wide mission-related entries |
| Fonts | Kairos Sans / Poppins | System fonts and installed CJK fallback |
| Palette | Pale/olive and dark bands | Pale green, charcoal and lime |
| Mobile figures | Reference-specific product crops | Original NORM frames, with enlargement |

These numerical values are CSS/reference settings, not a pixel-similarity score.
Actual screenshots show different line breaks, page lengths, media brightness and
image proportions because the NORM content and captures differ. The original
Windows title bars and application states remain visible. There is no video
motion or claim of an exact reproduction.

## Missing assets and dependencies

- No NORM flight film, real-aircraft hero photography or completed mission capture was supplied.
- No populated mission draft, connected telemetry or current successful AI connection capture was supplied.
- No Chinese-language application screenshots were supplied.
- Reference fonts, external Webflow CSS/JS, CDN images and videos were not supplied as local dependencies. DOM and request logs do not form a complete offline mirror. The private comparison package lists the discovered external URLs individually in `dependencies.json`.
- All NORM runtime assets are local. UFORCE branding, screenshots, DOM, tracking scripts and other reference materials are excluded from `dist/` and the public repository.

## Executed checks

| Check | Result |
| --- | --- |
| Build and complete translation keys | PASS — 26 pages |
| Static links, resources, anchors, canonical/OG/hreflang and sitemap | PASS — 692 local references, 50 anchors, 24 sitemap URLs |
| Asset hashes, SVG syntax, CSS balance, reference/credential leak scan | PASS |
| Python compilation and JavaScript syntax | PASS |
| Six original screenshots, Pages workflow, domain and CNAME preservation | PASS — byte/config comparison |
| Before/after home and Platform at 1440/768/390 | PASS — 36 comparison PNGs; before EN, after EN+ZH; plus 24 download/contact PNGs |
| All 26 routes at all three widths | PASS — 78 route/layout/resource cases |
| Root horizontal overflow and loaded images on captured pages | PASS |
| Mobile menu, Escape, screenshot dialog and focus return | PASS |
| Workflow click, same-route language switch, contact/download navigation, email destinations and Platform CTA | PASS |
| Console errors, uncaught page errors and HTTP errors during exercised routes | PASS — zero recorded errors |
| Firefox, Safari/WebKit and physical mobile devices | NOT_RUN |
| Public release location | PASS — public repository, non-draft pre-release and owner-uploaded installer |
| Anonymous installer URL / HTTP HEAD | PASS — HTTP 200 and expected 660,493,462-byte content length |
| Full application download, integrity audit and execution | NOT_RUN |
| End-to-end branded-email receipt | NOT_RUN |
| NORM application, hardware or real-aircraft testing | NOT_RUN |

`BROWSER_ACCEPTANCE.json` records the tested revision and check counts. Raw browser
results and screenshot artifacts are attached to the workflow run and included
in the private comparison package. Browser success proves the tested website
behavior in this environment, not email delivery or NORM product acceptance.
