#!/usr/bin/env python3
"""Build the NORM informational site using only Python's standard library."""
from pathlib import Path
from html import escape
from datetime import datetime, timezone
import hashlib
import json
import math
import shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
CONFIG = json.loads((ROOT / 'site.config.json').read_text())
DOMAIN = CONFIG['domain']
BASE = 'https://' + DOMAIN
EMAIL_READY = CONFIG.get('email_verified') is True
OPERATOR = CONFIG.get('operator_name')
RELEASE = CONFIG.get('public_release') is True
if RELEASE and (not EMAIL_READY or not OPERATOR):
    raise SystemExit('Public release requires verified contact and confirmed operator identity.')

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
for folder in ('assets', 'css', 'js'):
    shutil.copytree(ROOT / 'src' / folder, DIST / folder)

def put(path, text):
    target = DIST / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')

LOGO = '<svg viewBox="0 0 30 32" aria-hidden="true"><path fill="currentColor" d="M1 31V1h7l14 19V1h7v30h-7L8 12v19z"/></svg>'
put('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#101a17"/><path fill="#d1f06f" d="M14 49V15h8l20 22V15h8v34h-8L22 27v22z"/></svg>')

def route_art():
    contours = []
    for n in range(15):
        pts=[]
        for i in range(101):
            a=i*2*math.pi/100
            radius=55+n*14+11*math.sin(3*a+n*.23)+8*math.cos(5*a)
            x=390+radius*math.cos(a)*1.2
            y=275+radius*math.sin(a)*.82
            pts.append(f'{x:.1f},{y:.1f}')
        contours.append(f'<polyline points="{" ".join(pts)}"/>')
    circles=''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#d1f06f"/><circle cx="{x}" cy="{y}" r="13" fill="none" stroke="#d1f06f" opacity=".3"/><text x="{x+17}" y="{y-15}" fill="#dbe4d9" font-size="12">{i:02d}</text>' for i,(x,y) in enumerate([(135,386),(220,156),(445,119),(538,289),(376,430)],1))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="660" height="580" viewBox="0 0 660 580" role="img" aria-labelledby="t d"><title id="t">Illustrated waypoint plan</title><desc id="d">An original conceptual waypoint route over abstract contour lines. This is not a product screenshot, flight record, or navigable map.</desc><defs><pattern id="grid" width="55" height="55" patternUnits="userSpaceOnUse"><path d="M55 0H0V55" fill="none" stroke="#8dab94" stroke-opacity=".1"/></pattern></defs><rect x="15" y="30" width="630" height="500" fill="#17271d"/><rect x="15" y="30" width="630" height="500" fill="url(#grid)"/><g stroke="#809b73" opacity=".32" fill="none" stroke-width="1">{''.join(contours)}</g><path d="M135 386L220 156L445 119L538 289L376 430Z" fill="#d1f06f" fill-opacity=".045" stroke="#d1f06f" stroke-width="2.5"/><path d="M135 386L376 430" stroke="#d1f06f" stroke-width="2.5" stroke-dasharray="7 8"/><g font-family="monospace">{circles}<text x="38" y="62" fill="#b7cabc" font-size="11" letter-spacing="2">WAYPOINT PLAN / ILLUSTRATION</text><text x="38" y="505" fill="#a1b8a8" font-size="10" letter-spacing="1">CONCEPTUAL ROUTE · NO LIVE VEHICLE</text></g><g transform="translate(291 145) rotate(80)"><path d="M0 -24L5 -6L26 6V11L5 6L4 22L12 28V31L0 26L-12 31V28L-4 22L-5 6L-26 11V6L-5 -6Z" fill="#e4ece0"/></g><path d="M15 55V30H40M620 30H645V55M645 505V530H620M40 530H15V505" stroke="#b8cec1" fill="none" stroke-width="2"/><g transform="translate(440 472)"><rect width="178" height="36" fill="#d1f06f"/><text x="14" y="23" font-family="monospace" font-size="11" fill="#101a17">FOR OPERATOR REVIEW ↗</text></g></svg>'''
put('assets/waypoint-plan.svg', route_art())

def architecture_art():
    nodes=[(30,55,'01 / TASK','Mission requirements'),(30,185,'02 / AI ASSISTANCE','Interpret & propose'),(30,315,'03 / OPERATOR','Review & edit waypoints'),(30,445,'04 / APPROVAL','Decide what proceeds')]
    parts=[]
    for x,y,small,title in nodes:
        parts.append(f'<rect x="{x}" y="{y}" width="490" height="90" fill="#eef0e9" stroke="#a6b9a3"/><text x="{x+22}" y="{y+27}" font-size="11" font-family="monospace" letter-spacing="2" fill="#55674e">{small}</text><text x="{x+22}" y="{y+61}" font-size="23" font-family="Arial" fill="#17231b">{escape(title)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="680" viewBox="0 0 900 680" role="img" aria-labelledby="t"><title id="t">Mission workspace responsibilities and the device validation boundary</title><defs><marker id="a" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#54714d"/></marker></defs>{''.join(parts)}<g stroke="#54714d" fill="none" marker-end="url(#a)"><path d="M275 145v34M275 275v34M275 405v34"/><path d="M520 490H670V380"/></g><rect x="570" y="230" width="300" height="140" fill="#17271d"/><text x="595" y="265" fill="#d1f06f" font-family="monospace" font-size="11" letter-spacing="1.5">MISSION RECORDS</text><text x="595" y="303" fill="#eef0e9" font-family="Arial" font-size="22">Keep the task context</text><text x="595" y="334" fill="#b8cec1" font-family="Arial" font-size="17">alongside device records.</text><path d="M30 573H870" stroke="#789071" stroke-dasharray="7 6"/><text x="30" y="608" font-family="monospace" font-size="12" letter-spacing="1" fill="#3f533b">REAL-FLIGHT-CONTROLLER PATH</text><text x="30" y="639" font-family="Arial" font-size="21" fill="#17231b">Acceptance testing is still in progress.</text></svg>'''
put('assets/workspace-architecture.svg', architecture_art())

STEPS = [
 ('Mission brief','Start with the task.','Bring the mission requirements into the workspace so the proposed plan can be reviewed against the original request.'),
 ('AI-assisted planning','Turn the brief into a proposal.','AI helps interpret the request and propose a mission plan. The proposal remains a draft for the operator to examine.'),
 ('Waypoint editing','Review the route in detail.','Review and edit the proposed waypoints before deciding whether the plan is ready for approval.'),
 ('Operator approval','Keep the decision with the operator.','Actions involving a vehicle require human approval. Approval is separate from the AI’s suggestion and from verification of the device result.'),
 ('Mission records','Keep the task and its records together.','Keep device mission records alongside the planning workflow. Full real-device transfer, verification, and limited control are still undergoing acceptance testing.')
]

def graphic(index):
    if index==0:
        inside='<rect x="62" y="12" width="156" height="140" fill="none" stroke="#b8cec1"/><path d="M85 44H182M85 66H195M85 88H165M85 110H182" stroke="#d1f06f" stroke-width="3"/><path d="M201 12V30H218" fill="none" stroke="#b8cec1"/>'
    elif index==1:
        inside='<path d="M37 90H100M180 90H245M140 34V58M140 122V148" stroke="#809c80"/><rect x="107" y="57" width="66" height="66" transform="rotate(45 140 90)" stroke="#d1f06f" fill="none"/><circle cx="37" cy="90" r="9" fill="#d1f06f"/><circle cx="245" cy="90" r="9" fill="#d1f06f"/><text x="128" y="96" fill="#eef0e9" font-family="monospace" font-size="19">AI</text>'
    elif index==2:
        inside='<path d="M35 130L90 40L194 55L245 129Z" fill="none" stroke="#d1f06f" stroke-width="2"/><g fill="#d1f06f"><circle cx="35" cy="130" r="6"/><circle cx="90" cy="40" r="6"/><circle cx="194" cy="55" r="6"/><circle cx="245" cy="129" r="6"/></g><circle cx="194" cy="55" r="20" fill="none" stroke="#b8cec1" stroke-dasharray="3 4"/>'
    elif index==3:
        inside='<circle cx="140" cy="50" r="22" stroke="#b8cec1" fill="none"/><path d="M90 129V115a50 42 0 0 1 100 0v14" stroke="#b8cec1" fill="none"/><path d="M117 114L135 132L169 95" stroke="#d1f06f" fill="none" stroke-width="5"/>'
    else:
        inside='<path d="M73 30H220V148H73Z" fill="none" stroke="#b8cec1"/><path d="M59 132V16H206M45 117V2H192" fill="none" stroke="#6d856e"/><path d="M95 58H197M95 83H178M95 108H191" stroke="#d1f06f" stroke-width="3"/>'
    return f'<svg class="step-graphic" viewBox="0 0 280 170" aria-hidden="true">{inside}</svg>'

def workflow():
    buttons=''.join(f'<li><button class="step-button" type="button" data-step="{i}" aria-pressed="{"true" if i==0 else "false"}" aria-controls="flow-panel-{i}"><span class="step-num">0{i+1}</span><span>{s[0]}</span><span class="step-arrow" aria-hidden="true">↗</span></button></li>' for i,s in enumerate(STEPS))
    panels=''.join(f'<div class="step-panel" data-panel="{i}" id="flow-panel-{i}" {"hidden" if i else ""}>{graphic(i)}<span class="badge">Illustrated workflow · 0{i+1}</span><h3>{s[1]}</h3><p>{s[2]}</p></div>' for i,s in enumerate(STEPS))
    fallback=''.join(f'<div class="column"><span class="mono">0{i+1} / {s[0]}</span><h3>{s[1]}</h3><p>{s[2]}</p></div>' for i,s in enumerate(STEPS))
    return f'<div data-workflow class="workflow-enhanced"><div class="workflow-split"><div><div class="eyebrow">The mission workflow</div><h2>From a brief<br>to a reviewed plan.</h2><ol class="workflow-list" aria-label="Explore workflow stages">{buttons}</ol></div><div aria-live="polite">{panels}</div></div></div><div class="workflow-fallback"><div class="eyebrow">The mission workflow</div><h2>From a brief to a reviewed plan.</h2><div class="columns">{fallback}</div></div>'

def btn(label, href, secondary=False):
    return f'<a class="button{" secondary" if secondary else ""}" href="{href}">{label}<span aria-hidden="true">↗</span></a>'
def textlink(label,href):
    return f'<a class="text-link" href="{href}">{label}<span aria-hidden="true">↗</span></a>'
def section(body,dark=False,extra=''):
    return f'<section class="section{" dark" if dark else ""} {extra}"><div class="wrap">{body}</div></section>'
def feature_rows(items):
    return ''.join(f'<article class="feature-row"><span class="section-number">0{i+1}</span><div><h3>{title}</h3><p>{text}</p></div></article>' for i,(title,text) in enumerate(items))
def columns(items):
    return '<div class="columns">'+''.join(f'<article class="column"><span class="mono">0{i+1} / {tag}</span><h3>{title}</h3><p>{text}</p></article>' for i,(tag,title,text) in enumerate(items))+'</div>'

PAGES={
 'index.html':('AI-assisted drone mission planning','NORM brings mission briefs, AI-assisted planning, waypoint editing, operator approval, and device mission records into one workspace for fixed-wing waypoint missions.'),
 'platform/index.html':('Platform','Explore the NORM mission workspace: task requirements, AI-assisted proposals, waypoint editing, operator approval, and device mission records.'),
 'workflow/index.html':('Mission workflow','Follow the NORM workflow from the mission brief through AI-assisted planning, waypoint review, operator approval, and mission records.'),
 'governance/index.html':('Operator approval','AI helps propose a mission. The operator reviews and approves actions involving a vehicle. Learn how NORM describes this boundary.'),
 'evidence/index.html':('Development status','Project-reported development status for NORM: a packaged Windows preview, workflow tests, and real-flight-controller acceptance work in progress.'),
 'architecture/index.html':('Workspace architecture','A conceptual view of the responsibilities in NORM: mission requirements, AI proposals, waypoint review, operator approval, and device records.'),
 'integrations/index.html':('Flight-controller integration','Real-flight-controller integration is in progress. Read the current scope of serial connection, initialization, mission retrieval, and verification work.'),
 'updates/index.html':('Project updates','Current NORM development notes: the Windows preview, task and draft workflows, product entry points, and flight-controller validation.'),
 'contact/index.html':('Contact','Contact information and engineering evaluation topics for the NORM AI-assisted drone mission workspace.'),
 'legal/privacy/index.html':('Privacy notice','Information about data handling on this static NORM preview website, including the absence of forms, analytics, and model connections.'),
 'legal/terms/index.html':('Website notes','Scope of the NORM informational preview website, product descriptions, illustrative diagrams, and engineering preview status.'),
 '404.html':('Page not found','The requested NORM page could not be found. Return to the homepage or explore the mission workspace.')
}

def render(path):
    depth=len(Path(path).parts)-1
    prefix='../'*depth or './'
    L=lambda target: prefix+target
    title,description=PAGES[path]
    canonical=BASE+('/' if path=='index.html' else '/'+path.replace('index.html',''))
    nav_items=[('platform/index.html','Platform'),('workflow/index.html','Workflow'),('governance/index.html','Governance'),('evidence/index.html','Development')]
    nav=''
    for target,label in nav_items:
        current=' aria-current="page"' if target==path else ''
        nav+=f'<a href="{L(target)}"{current}>{label}</a>' 
    head=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | NORM</title><meta name="description" content="{escape(description,quote=True)}"><meta name="robots" content="{"index,follow" if RELEASE and path!='404.html' else "noindex,follow"}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:site_name" content="NORM"><meta property="og:title" content="{escape(title)} | NORM"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/assets/og/norm-preview.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="NORM — AI-assisted drone mission workspace"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#101a17"><link rel="icon" href="{L('favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{L('css/site.css')}"><script src="{L('js/site.js')}" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="{L('index.html')}" aria-label="NORM home">{LOGO}<span>NORM</span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button><nav class="site-nav" id="site-nav" aria-label="Main navigation"><div class="nav-links">{nav}</div><a class="nav-contact" href="{L('contact/index.html')}">Contact<span aria-hidden="true">↗</span></a></nav></header><main id="main">'''

    def hero(eyebrow,headline,intro,index):
        return f'<section class="hero page-hero"><div class="wrap"><div class="page-topline"><div class="eyebrow">{eyebrow}</div><span class="mono page-index">NORM / {index:02}</span></div><h1>{headline}</h1><p class="lead">{intro}</p></div></section>'

    if path=='index.html':
        content=f'''<section class="hero"><div class="wrap"><div class="hero-grid"><div><div class="eyebrow">NORM / Windows preview</div><h1>A clearer path<br>from <span>brief</span><br>to <span>mission.</span></h1><p class="lead">An AI-assisted drone mission workspace.<br>Bring the brief, proposed plan, waypoints, and operator review together.</p><div class="actions">{btn('Explore the workspace',L('platform/index.html'))}{textlink('Development status',L('evidence/index.html'))}</div></div><figure class="hero-art"><img src="{L('assets/waypoint-plan.svg')}" width="660" height="580" alt="Conceptual fixed-wing waypoint plan over abstract contour lines"><figcaption>Workflow illustration · Not a live product view</figcaption></figure></div><div class="hero-strip mono"><span>Mission scope / <b>Fixed-wing waypoints</b></span><span>Decision / <b>Operator approval</b></span><span>Stage / <b>Engineering preview</b></span></div></div></section>'''
        content+=section(f'<div class="editorial"><div><div class="eyebrow">A workspace for the whole plan</div><h2>Keep the task<br>in view.</h2><p class="lead" style="margin-top:25px">A mission starts with a request. NORM brings the work of turning that request into a reviewable plan into one place.</p>{textlink("Inside the platform",L("platform/index.html"))}</div><div>'+feature_rows([('Understand the brief.','Use AI assistance to interpret the task and develop a proposed plan.'),('Work through the waypoints.','Review and edit the proposed route, keeping the task requirements alongside the plan.'),('Make the decision.','Operator approval remains separate from AI suggestions. Actions involving a vehicle need human approval.')])+'</div></div>')
        content+=section(workflow()+f'<div class="actions">{textlink("Explore the workflow",L("workflow/index.html"))}</div>',True)
        content+=f'<section class="status-band"><div class="wrap status-inner"><div><div class="eyebrow">Current development stage</div><h2>Windows preview.<br>Engineering in progress.</h2></div><div><p>The project reports a packaged preview for demonstrations and engineering evaluation. Real-flight-controller validation is still in progress; the real-aircraft execution workflow has not completed acceptance.</p>{textlink("Read the development status",L("evidence/index.html"))}</div></div></section>'
        content+=section(f'<div class="section-head"><div><div class="eyebrow">A deliberate division of responsibility</div><h2>AI proposes.<br>The operator approves.</h2></div><div><p class="lead">A useful proposal gives the operator something concrete to examine. It does not establish that a vehicle received a mission or carried it out.</p>{textlink("Review the approval boundary",L("governance/index.html"))}</div></div>')
    elif path=='platform/index.html':
        content=hero('The platform','One workspace.<br>A mission you can review.','NORM brings task requirements, AI-assisted planning, waypoint editing, operator approval, and device mission records into one workflow.',1)
        content+=section(f'<div class="section-head"><h2>Built around<br>fixed-wing waypoints.</h2><p class="lead">Keep the original request close to the proposed plan. Examine the waypoints, make edits, and decide what should proceed.</p></div><figure class="picture-section"><img src="{L("assets/waypoint-plan.svg")}" width="660" height="580" alt="Original illustration of a proposed waypoint route" style="max-height:540px"><figcaption class="figure-caption"><span>Illustrated planning concept. This is not a screenshot of the Windows application.</span><span class="mono">01 / Mission workspace</span></figcaption></figure>')
        content+=section('<div class="editorial"><div><div class="eyebrow">The work, kept together</div><h2>From requirements<br>to records.</h2></div><div>'+feature_rows([('Tasks and drafts','Organize the mission requirements and proposed plans in the same workspace.'),('AI-assisted planning','Use AI to help interpret the task and propose a plan for review.'),('Waypoint editing','Review and edit the waypoints before approval.'),('Approval and records','Keep operator approval and device mission records in the planning workflow. Device-side acceptance work is ongoing.')])+'</div></div>')
        content+=section(f'<div class="section-head"><h2>Explore the current<br>Windows preview.</h2><div><p class="lead">The project reports that the packaged application can be started and demonstrated. Task and draft-management workflows have been tested; real-aircraft execution acceptance is not complete.</p>{textlink("What has been reported",L("evidence/index.html"))}</div></div>',True)
    elif path=='workflow/index.html':
        content=hero('The mission workflow','Draft. Review.<br>Decide what proceeds.','Follow the planning process from the mission brief to operator approval and mission records. Each stage has a distinct purpose.',2)
        content+=section(workflow(),True)
        content+=section('<div class="section-head"><h2>Review the plan.<br>Verify the result.</h2><p class="lead">The planning workflow and the device result answer different questions. A plan can be ready for review while hardware acceptance remains incomplete.</p></div>'+columns([('Draft','Does it match the task?','Check the proposed mission against the requirements and examine the waypoint edits.'),('Decision','Has the operator approved it?','Approval is a human decision. An AI suggestion does not grant itself permission to act.'),('Device result','What happened on the device?','Mission retrieval, independent upload verification, and limited control still need their applicable acceptance checks.')]))
        content+=section(f'<div class="callout"><span class="symbol" aria-hidden="true">↗</span><div><h3>The illustration describes the workflow.</h3><p>It does not show a completed hardware upload or flight. The real-flight-controller path is still undergoing acceptance testing.</p>{textlink("See the current integration scope",L("integrations/index.html"))}</div></div>')
    elif path=='governance/index.html':
        content=hero('Operator approval','AI proposes.<br>The operator approves.','NORM uses AI to help understand a task and suggest a plan. Actions involving a vehicle still require human approval.',3)
        content+=section('<div class="editorial"><div><div class="eyebrow">The approval boundary</div><h2>A proposal is<br>a starting point.</h2></div><div>'+feature_rows([('AI assistance','The model helps interpret the task and propose a plan. Its output remains subject to review.'),('Operator judgment','The operator examines the plan and decides whether to approve the relevant device actions.'),('Device verification','Approval alone does not prove delivery or execution. Device-side results need their own verification.')])+'</div></div>')
        content+=section('<div class="section-head"><h2>Permission and outcome<br>are separate questions.</h2><p class="lead">Human approval defines who makes the decision. Acceptance testing establishes what a particular configuration actually did.</p></div><div class="wide-note"><p>Full mission retrieval, independent verification after AI-generated waypoint uploads, and subsequent limited control have not all passed acceptance testing.</p></div>',True)
        content+=section(f'<div class="section-head"><h2>Read the boundary<br>alongside the evidence.</h2><div><p class="lead">The current project summary describes a Windows engineering preview. It does not establish production qualification or end-to-end real-aircraft execution acceptance.</p>{textlink("Development status",L("evidence/index.html"))}</div></div>')
    elif path=='evidence/index.html':
        content=hero('Evidence & development','Where the preview stands.','A concise account of the current project-reported status, with software progress and real-hardware acceptance kept distinct.',4)
        rows=[('Windows preview','Project reported','The application is packaged and can be started and demonstrated.',''),('Task and draft workflows','Tests reported','The project reports tests for task and draft-management workflows. No test totals or build-bound results are published here.',''),('Serial connection and initialization','Partial validation','Some real-hardware connection and initialization checks are reported as complete. This does not establish mission transfer or execution.','pending'),('Mission retrieval, upload verification, limited control','Acceptance incomplete','Full mission retrieval, independent verification after AI-generated waypoint uploads, and subsequent limited control have not all passed acceptance.','pending'),('Interrupted mission read','Hardware retest pending','A script state-handling issue was identified. An offline fix and regression checks are reported as complete; the hardware retest is the next step.','pending')]
        body=''.join(f'<tr><td>{area}</td><td><span class="badge {cls}">{status}</span></td><td><p>{detail}</p></td></tr>' for area,status,detail,cls in rows)
        content+=section(f'<div class="eyebrow">Project-reported development status</div><div class="table-wrap"><table><caption class="small" style="text-align:left;padding:0 18px 25px">Status summarized from the supplied project description. These statements are not an independent test certification.</caption><thead><tr><th scope="col">Area</th><th scope="col">Status</th><th scope="col">Scope</th></tr></thead><tbody>{body}</tbody></table></div><div class="wide-note"><p><strong>Release identity and public evidence</strong></p><p>A final build identifier, version-bound test reports, and the actual release date have not been supplied for this public summary. No public evidence download or independent verification claim is made here.</p></div>')
        content+=section(f'<div class="section-head"><h2>The next result<br>needs real hardware.</h2><div><p class="lead">Offline repair and regression checks address the reported script issue. Hardware retesting is still needed to establish the result on the flight controller.</p>{textlink("Read integration scope",L("integrations/index.html"))}</div></div>',True)
    elif path=='architecture/index.html':
        content=hero('Workspace architecture','Distinct responsibilities.<br>A shared task context.','A conceptual view of how the mission brief, AI proposals, waypoint review, approval, and device mission records fit together.',5)
        content+=section(f'<figure class="architecture-figure"><img src="{L("assets/workspace-architecture.svg")}" width="900" height="680" alt="Conceptual workflow from requirements to AI proposals, waypoint review, operator approval, and device mission records, with the hardware path under acceptance testing"><figcaption>Workflow illustration, not a live product view or an internal module specification.</figcaption></figure>')
        content+=section(columns([('Task context','Keep the brief attached.','The requirements provide the context against which a proposed plan can be reviewed.'),('Plan review','Separate assistance and decision.','AI-generated suggestions and operator approval have different roles in the workflow.'),('Device path','Establish the actual result.','Device mission records belong alongside the planning process. Hardware acceptance remains in progress.')] ))
        content+=section(f'<div class="callout"><span class="symbol" aria-hidden="true">↗</span><div><h3>Integration has its own evidence requirements.</h3><p>This conceptual diagram does not promise support for every autopilot, protocol, or flight-controller configuration.</p>{textlink("Read integration scope",L("integrations/index.html"))}</div></div>')
    elif path=='integrations/index.html':
        content=hero('Flight-controller integration','Connect the plan<br>to the device. Carefully.','Real-flight-controller integration is in progress. The current project summary reports partial serial-connection and initialization validation.',6)
        content+=section('<div class="editorial"><div><div class="eyebrow">Current engineering scope</div><h2>Connection is<br>the first step.</h2></div><div>'+feature_rows([('Serial connection and initialization','Partial checks have been reported on real hardware. These results cover a limited part of the device workflow.'),('Mission retrieval','Full mission reading remains part of the acceptance work. A recent interruption was traced to script state handling.'),('Upload verification and limited control','Independent checks after AI-generated waypoint uploads and subsequent limited control have not all passed acceptance.')])+'</div></div>')
        content+=section('<div class="section-head"><h2>Compatibility needs<br>a defined configuration.</h2><p class="lead">A public compatibility matrix has not been established from the supplied current description. The site does not promise support for every flight controller or autopilot.</p></div><div class="wide-note"><p>For engineering evaluation, the relevant configuration includes the flight controller, firmware, connection, mission type, and the behavior being checked. A successful connection alone cannot establish the rest of that workflow.</p></div>',True)
        content+=section(f'<div class="section-head"><h2>Follow the work<br>through acceptance.</h2><div><p class="lead">Read the reported software progress and the remaining hardware checks together.</p>{textlink("Development status",L("evidence/index.html"))}</div></div>')
    elif path=='updates/index.html':
        content=hero('Development notes','The work in progress.','Current project-reported notes for the Windows preview. No dated release announcement is being made on this page.',7)
        entries=[('PREVIEW','A packaged Windows application.','The project reports that the Windows preview can be started and demonstrated for engineering evaluation. Task and draft-management workflows have been tested.'),('INTEGRATION','Bring the entry points and device workflow together.','Work continues on the product entry points and real-flight-controller integration. Some serial connection and initialization checks have been completed.'),('NEXT CHECK','Retest the interrupted mission read on hardware.','The recent read interruption was traced to script state-handling logic. The offline repair and regression checks are reported as complete. The real-hardware retest remains next.')]
        content+=section('<div class="timeline">'+''.join(f'<article class="timeline-item"><span class="mono">{tag}</span><div><h3>{title}</h3><p>{text}</p></div></article>' for tag,title,text in entries)+f'<div class="wide-note"><p>These are development notes, not a dated changelog. The final preview’s release date and build identity have not been provided.</p>{textlink("Full development status",L("evidence/index.html"))}</div></div>')
    elif path=='contact/index.html':
        content=hero('Contact','Let’s talk about<br>the mission workflow.','Product questions, engineering evaluation, and integration discussions for the NORM Windows preview.',8)
        if EMAIL_READY:
            panel=f'<span class="badge">Email contact</span><h2>Start a conversation.</h2><a class="email text-link" href="mailto:{escape(CONFIG["email"])}">{escape(CONFIG["email"])}</a><p class="small" style="margin-top:25px">Include your mission type and what you would like to evaluate.</p>'
        else:
            panel='<span class="badge">Contact channel in preparation</span><h2>The public inbox<br>is being set up.</h2><p>Direct inquiries will be available here once the contact channel is ready. There is no submission form in this preview.</p>'
        content+=section(f'<div class="contact-grid"><div class="contact-panel">{panel}</div><div><div class="eyebrow">Before an evaluation</div><h3>Start with a specific question.</h3><div style="margin-top:25px">'+feature_rows([('Your mission','What are you trying to plan, and which part of the workflow would you like to evaluate?'),('Your configuration','Which aircraft, flight controller, and connection are relevant to the evaluation?'),('The current scope','Review the engineering preview status and the remaining hardware acceptance checks.')])+f'</div>{textlink("Read development status",L("evidence/index.html"))}</div></div>')
    elif path=='legal/privacy/index.html':
        content=hero('Website information','Privacy notice.','How this informational website is built and what data-handling functions it contains.',9)
        operator=f'<h2>Website operator</h2><p>{escape(OPERATOR)}. Contact: <a href="mailto:{escape(CONFIG["email"])}">{escape(CONFIG["email"])}</a>.</p>' if OPERATOR and EMAIL_READY else '<div class="legal-status">Preview notice. The public operator details and contact channel still need to be confirmed before this notice can be finalized.</div>'
        content+=section(f'<div class="prose">{operator}<h2>The website itself</h2><p>This static preview contains no account registration, contact submission form, advertising tags, analytics scripts, or model API connection. The site code does not set cookies or use browser storage.</p><h2>Hosting requests</h2><p>Loading a hosted website sends technical request data, such as an IP address and browser information, to the hosting and network providers. This website is prepared for GitHub Pages and Cloudflare; the operator must confirm the deployed configuration and applicable provider information before final publication.</p><h2>Contact</h2><p>When an email contact is enabled, selecting an email link opens your own mail application. The website does not send a message automatically. The handling of any correspondence must be described with the confirmed operator and contact details.</p><h2>Changes</h2><p>This notice must be reviewed if forms, analytics, accounts, or other data-handling features are added. The final notice will identify the operator and the applicable contact details.</p></div>')
    elif path=='legal/terms/index.html':
        content=hero('Website information','Website notes.','The scope of this preview website and its product information.',10)
        content+=section('<div class="prose"><div class="legal-status">Preview notes. Operator details and any formal terms for software evaluation are not finalized here.</div><h2>Informational purpose</h2><p>This website introduces NORM, an AI-assisted drone mission workspace focused on fixed-wing waypoint missions. It does not provide vehicle control, an online mission planner, a product download, or a software license.</p><h2>Engineering preview</h2><p>Product progress is described as project-reported status. A packaged application and workflow tests do not establish completed acceptance of the real-aircraft execution workflow.</p><h2>Illustrations</h2><p>Route and workflow graphics are explanatory illustrations. They are not live product views, flight records, verified maps, or instructions for operating an aircraft.</p><h2>Evaluation arrangements</h2><p>Availability, configuration, software permissions, and evaluation arrangements would need to be agreed separately with the confirmed project operator. These website notes do not create a purchase or evaluation agreement.</p></div>')
    else:
        content=f'<section class="hero"><div class="wrap not-found"><div class="big-number">404</div><div><div class="eyebrow">Page not found</div><h1>This page<br>isn’t here.</h1><p class="lead">Return to the homepage or explore the workspace.</p><div class="actions">{btn("Return home",BASE+"/")}{btn("Explore the platform",BASE+"/platform/",True)}</div></div></div></section>'
    groups=[('Explore',[('platform/index.html','Platform'),('workflow/index.html','Workflow'),('governance/index.html','Governance')]),('Engineering',[('architecture/index.html','Architecture'),('integrations/index.html','Integrations'),('evidence/index.html','Development status')]),('Project',[('updates/index.html','Updates'),('contact/index.html','Contact')])]
    footer_groups=''.join('<div><span class="mono">'+group+'</span>'+''.join(f'<a href="{L(link)}">{name}</a>' for link,name in items)+'</div>' for group,items in groups)
    footer=f'</main><footer class="footer"><div class="wrap"><div class="footer-top"><p>An AI-assisted drone mission workspace.<br><span class="small">Windows preview · Fixed-wing waypoint missions</span></p><nav class="footer-groups" aria-label="Footer navigation">{footer_groups}</nav></div><div class="footer-wordmark" aria-hidden="true">NORM↗</div><div class="footer-bottom"><span>NORM · Engineering preview</span><div><a href="{L("legal/privacy/index.html")}">Privacy notice</a><a href="{L("legal/terms/index.html")}">Website notes</a><a href="#main">Back to top ↑</a></div></div></div></footer></body></html>'
    if path=='404.html':
        # Self-contained error page: assets work at any missing nested path and offline.
        css=(ROOT/'src/css/site.css').read_text()
        content=content.replace('</div></div></div></section>',f'<p class="small" style="margin-top:28px">Viewing this file offline? <a class="text-link" href="index.html">Open the local homepage</a>.</p></div></div></div></section>')
        head=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | NORM</title><meta name="description" content="{description}"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}/404.html"><meta property="og:title" content="Page not found | NORM"><meta property="og:description" content="{description}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}/404.html"><meta property="og:image" content="{BASE}/assets/og/norm-preview.png"><style>{css}</style></head><body><main id="main">'
        footer='</main></body></html>'
    put(path,head+content+footer)

for page in PAGES:
    render(page)
put('.nojekyll','')
put('CNAME', DOMAIN+'\n')
put('robots.txt',f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
urls=[BASE+('/' if p=='index.html' else '/'+p.replace('index.html','')) for p in PAGES if p!='404.html']
put('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>\n')
manifest={'artifact':'NORM static website preview','generated_at':datetime.now(timezone.utc).isoformat(),'domain':DOMAIN,'page_count':len(PAGES),'public_release':RELEASE,'contact_verified':EMAIL_READY,'product_verification':'NOT_PERFORMED','files':{p.relative_to(DIST).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DIST.rglob('*')) if p.is_file()}}
put('BUILD_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
print(f'Built {len(PAGES)} pages in dist/; public_release={RELEASE}; contact_verified={EMAIL_READY}')
