# NORM visual revision — 2026-10-17

## Review state

- Existing repository: `Lsofimeow/norm-website`.
- Isolated branch: `design/uforce-reference-v2`.
- Baseline: `3765a453ab6152c86e28e70fc873ff930a3ffabe`.
- Existing 12 English routes retained; 12 corresponding Chinese routes added under `/zh/`.
- No changes to the Pages workflow, CNAME, domain, DNS, Cloudflare, payment or production branch.
- This is implemented source awaiting browser visual acceptance, not a production deployment.

## What changed

The homepage and existing Platform page now use a centered headline over full-width
application imagery, large editable media sections, alternating pale/dark bands,
a vertical sequence of wide image-led entries, and a large NORM footer. Shared
navigation, typography, spacing, contact links and responsive rules apply to the
remaining pages. The existing workflow interaction and route structure remain.

The visual reference was the original UFORCE home/C2 desktop, tablet and mobile
captures, rendered HTML and engineering records. The old NORM source used a
left-aligned headline and an abstract route illustration. That source-level
comparison informed the revision; same-width browser captures of old/new NORM
could not be executed in this environment. No pixel-match claim is made.

Six owner-supplied NORM captures are used unchanged. Large figures can be opened
in a dialog, closed with Escape, and inspected horizontally on small screens.
Captured disconnected/empty/expired/warning states are described in captions.
The images do not establish aircraft execution or device-control acceptance.

The English and Chinese versions use explicit static routes, editable translation
entries, translated metadata, accessible labels and conceptual diagrams. Language
switches preserve the current route; no browser storage or remote translation is
used. Product screenshot pixels remain in their original English language.

`hello@normautonomy.com` appears on the contact page, homepage/product contact
sections and shared footer. The owner requested publication. Destination
verification and routing are enabled; actual receipt remains untested.

## Reference parameters and deliberate differences

| Item | Captured reference | Revision |
| --- | --- | --- |
| Desktop container | 1296 px at 1440 px viewport | 1296 px maximum; 72 px side margins at 1440 |
| Hero heading | 72 px desktop; 44 px mobile | 72 px desktop; 44 px mobile; Chinese 64/40 px |
| Major spacing | About 120 px desktop; 60 px mobile | 110 px desktop; 60 px mobile |
| Main media | Full-width video and product imagery | Full-width owner-supplied static software captures |
| Product entrances | Vertical large-image sequence | Three wide mission-related entries |
| Typography | Kairos Sans / Poppins in capture records | System fonts; no supplied licensed local font files |
| Palette | Pale/olive and dark sections | NORM pale green, charcoal and lime accent |
| Mobile | Stacked large media and concise labels | Stacked figures; original screenshots can be enlarged |

These are source/CSS parameters, not measured post-render results. Exact line
breaks, perceived image scale, page height and tablet spacing need browser review.

## Missing assets / remaining gaps

- No NORM flight film, real-aircraft hero photography, or completed mission capture
  was supplied. The hero uses a real application still; no substitute flight claim.
- No additional populated-draft, connected-telemetry or current successful connection
  capture was supplied. Supplied screenshots retain their visible original states.
- No Chinese-language application captures were supplied. Site copy is translated;
  screenshots are not edited to simulate a Chinese application build.
- Reference font files, external Webflow CSS/JS, CDN images and video were not
  included as local dependencies in the archive. Request logs and DOM are not an
  offline mirror. The private comparison package lists individual missing URLs.
- New NORM runtime assets are local. Reference branding, captures, source DOM,
  analytics and scripts are excluded from `dist/` and this public repository.

## Executed checks

| Check | Result |
| --- | --- |
| Build both languages with complete translation keys | PASS — 24 pages |
| Local resource/link resolution, anchors, same-route language switches | PASS |
| Canonical/OG/hreflang metadata and sitemap | PASS — 22 sitemap URLs |
| Asset hashes, SVG syntax, CSS brace balance, reference/credential leak scan | PASS |
| Python compilation and JavaScript syntax | PASS |
| Original six PNGs compared byte-for-byte with supplied files | PASS |
| Pages workflow, domain values and CNAME compared with baseline | PASS |
| 1440 / 768 / 390 before/after browser screenshots | NOT_RUN |
| Mobile layout/overflow, menu, keyboard and dialog behavior in browser | NOT_RUN |
| Browser console, network errors and navigation clicks | NOT_RUN |
| End-to-end branded-email receipt | NOT_RUN |
| NORM software, hardware or real-flight testing | NOT_RUN |

The managed preview process failed before serving pages:
`bwrap: Can't mount proc on /newroot/proc: Operation not permitted`.
No browser acceptance result or before/after screenshots have been fabricated.
The private comparison package contains actual reference captures (lossless WebP copies for delivery) and same-width
live HTML frames for the baseline and revision, plus an optional local capture
script. The comparison frames are not screenshots or test evidence.
