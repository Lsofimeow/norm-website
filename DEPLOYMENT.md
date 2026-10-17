# Deployment configuration and status

Target: GitHub Pages origin; Cloudflare DNS and canonical redirects;
`hello@normautonomy.com` forwarded to a user-selected verified mailbox.

## 1. GitHub

Public source repository: Lsofimeow/norm-website.
GitHub Pages is enabled with GitHub Actions. The preview has been deployed successfully. The Pages custom domain is now
set to `normautonomy.com`. The apex HTTPS site returned HTTP 200, and
GitHub Enforce HTTPS is enabled. The apex A records remain DNS-only.
Cloudflare holds the canonical redirect rule; only the www CNAME uses its proxy.
Email Routing DNS is enabled and ready. The destination was verified on
2026-10-17, and the hello forwarding rule is enabled. An end-to-end receipt
test is still pending; the public contact link remains disabled until that check.

The Pages custom domain was saved before the DNS records were added. Verify domain ownership in GitHub where
available. Record the deployed commit, Actions run, and actual Pages URL.
`deployment_url` in `site.config.json` is now `https://normautonomy.com`. This value controls
canonical URLs, social images, the sitemap and absolute 404 recovery links;
regular navigation and assets use relative paths.

## 2. DNS and HTTPS

Read and save the existing Cloudflare DNS records before changing anything.
Modify only conflicting web-hosting records for `@` and `www` as necessary.
Preserve unrelated mail, verification and service records. Do not overwrite
an existing record set blindly.

GitHub's documented apex A records:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | lsofimeow.github.io |

The `www` CNAME target does not include the repository name. Set DNS-only
initially so GitHub can validate the domain and issue its certificate.
Check existing AAAA, ALIAS, CNAME and CAA records for certificate conflicts.
Do not add a wildcard record. Enable Enforce HTTPS once GitHub offers it.

After GitHub HTTPS and the Cloudflare edge certificate are active, use the
Cloudflare proxy for records that must be covered by Redirect Rules. Use
Full (strict) TLS to the GitHub origin; do not use Flexible mode. Verify
origin HTTPS before enabling the proxy. Preserve unrelated zone settings.

Current configuration: the four apex A records are DNS-only; only `www` is
proxied to serve its canonical redirect at the Cloudflare edge. The Cloudflare
universal certificate covering the apex and wildcard is active, and TLS mode
is Full (strict). Apex HTTP-to-HTTPS is provided by GitHub Pages.

## 3. Canonical redirect

Canonical URL: `https://normautonomy.com`.

Create a Single Redirect scoped to exactly these two hostnames:

```text
(http.host eq "www.normautonomy.com") or
(http.host eq "normautonomy.com" and not ssl)
```

Dynamic destination expression:

```text
concat("https://normautonomy.com", http.request.uri.path)
```

Status: 301. Preserve query string: enabled. HTTPS apex requests do not match,
so the rule has no self-redirect. Cloudflare redirect rules require proxied
traffic; a DNS-only record will bypass them. Review existing redirect rules
before adding this rule, and preserve unrelated rules.

Check root and nested pages through HTTP/HTTPS and apex/www; preserve the path
and query. Also check `/404-example/nested/` and confirm an actual 404 status.

## 4. Branded email routing

Create the custom incoming address `hello@normautonomy.com` in Cloudflare
Email Routing and route it to the destination mailbox selected by the user.
The destination was verified on 2026-10-17. The forwarding rule now matches
only `hello@normautonomy.com` and is enabled. Cloudflare reports Email Routing
as ready; catch-all remains off. End-to-end receipt has not yet been tested.

Inspect existing MX and SPF records first. Do not replace active mail hosting
without resolving the conflict. Use Cloudflare's actual generated MX/TXT
values; do not guess account-specific routing records or add a second SPF
record. Keep catch-all off unless it is specifically wanted.

The user must complete destination-address verification through the supplied
verification message. The result here is incoming forwarding; a normal
outgoing mailbox or the ability to reply as the branded address requires
separate configuration. Do not claim two-way mailbox service from a routing
rule alone. No paid mailbox subscription is included.

Only set `email_verified: true` after routing is active and receipt has been
checked. A test message must be authorized before sending it.

## Primary references checked for this build

- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://developers.cloudflare.com/rules/url-forwarding/single-redirects/create-dashboard/
- https://developers.cloudflare.com/rules/url-forwarding/examples/redirect-www-to-root/
- https://developers.cloudflare.com/email-service/configuration/email-routing-addresses/
