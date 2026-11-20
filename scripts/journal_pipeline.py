#!/usr/bin/env python3
"""Collect cross-repository GitHub evidence and build daily/weekly/monthly journal reports."""
from __future__ import annotations
import argparse, calendar, datetime as dt, hashlib, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
TZ=ZoneInfo("Asia/Shanghai")
API="https://api.github.com"
def read_json(path, default):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError): return default
def write_json(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def api_get(path, token=None):
    req=urllib.request.Request(API+path,headers={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"xm-journal-bot",**({"Authorization":f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req,timeout=25) as response: return json.loads(response.read().decode("utf-8"))
def api_pages(path, token=None, list_key=None, page_size=100, max_pages=5):
    collected=[]
    for page in range(1,max_pages+1):
        separator="&" if "?" in path else "?"
        data=api_get(f"{path}{separator}page={page}",token)
        items=data.get(list_key,[]) if list_key and isinstance(data,dict) else data
        if not isinstance(items,list): items=[]
        collected.extend(items)
        if len(items)<page_size: break
    return {list_key:collected} if list_key else collected
def day_bounds(day):
    start=dt.datetime.combine(day,dt.time.min,TZ); end=dt.datetime.combine(day+dt.timedelta(days=1),dt.time.min,TZ)
    return start.astimezone(dt.timezone.utc).isoformat().replace("+00:00","Z"),end.astimezone(dt.timezone.utc).isoformat().replace("+00:00","Z")
def date_of(value):
    if not value: return None
    try: return dt.datetime.fromisoformat(value.replace("Z","+00:00")).astimezone(TZ).date()
    except (ValueError,TypeError): return None
def collect_repo(repo, day, token):
    since,until=day_bounds(day); full=repo["full_name"]; encoded=urllib.parse.quote(full,safe="/")
    result={"repository":full,"slug":repo["slug"],"display_name":repo["display_name"],"url":f"https://github.com/{full}","commits":[],"pull_requests":[],"workflow_runs":[],"deployments":[],"errors":[]}
    requests=[
      ("commits",f"/repos/{encoded}/commits?since={urllib.parse.quote(since)}&until={urllib.parse.quote(until)}&per_page=100"),
      ("pulls",f"/repos/{encoded}/pulls?state=all&sort=updated&direction=desc&per_page=100"),
      ("workflows",f"/repos/{encoded}/actions/runs?created={urllib.parse.quote(since + chr(46) + chr(46) + until)}&per_page=100"),
      ("deployments",f"/repos/{encoded}/deployments?per_page=10")
    ]
    payload={}
    for key,path in requests:
        try:
            if key=="workflows": payload[key]=api_pages(path,token,"workflow_runs",100,5)
            else: payload[key]=api_pages(path,token,None,10 if key=="deployments" else 100,1 if key=="deployments" else 5)
        except Exception as exc: result["errors"].append({"source":key,"message":str(exc)[:240]}); payload[key]=[]
    for item in payload["commits"] if isinstance(payload["commits"],list) else []:
        commit=item.get("commit",{}); author=commit.get("author") or {}
        result["commits"].append({"sha":item.get("sha","")[:12],"message":(commit.get("message") or "").splitlines()[0][:180],"author":(author.get("name") or "unknown"),"date":author.get("date"),"url":item.get("html_url")})
    for item in payload["pulls"] if isinstance(payload["pulls"],list) else []:
        relevant=[item.get("created_at"),item.get("updated_at"),item.get("merged_at")]
        if any(date_of(v)==day for v in relevant):
            result["pull_requests"].append({"number":item.get("number"),"title":item.get("title"),"state":"merged" if item.get("merged_at") else item.get("state"),"created_at":item.get("created_at"),"updated_at":item.get("updated_at"),"merged_at":item.get("merged_at"),"url":item.get("html_url")})
    runs=payload["workflows"].get("workflow_runs",[]) if isinstance(payload["workflows"],dict) else []
    for item in runs:
        result["workflow_runs"].append({"id":item.get("id"),"name":item.get("name") or item.get("display_title"),"event":item.get("event"),"status":item.get("status"),"conclusion":item.get("conclusion"),"created_at":item.get("created_at"),"updated_at":item.get("updated_at"),"url":item.get("html_url")})
    for item in payload["deployments"] if isinstance(payload["deployments"],list) else []:
        created=date_of(item.get("created_at"))
        dep={"id":item.get("id"),"environment":item.get("environment"),"created_at":item.get("created_at"),"ref":item.get("ref"),"url":item.get("url"),"statuses":[]}
        try:
            statuses=api_get(f"/repos/{encoded}/deployments/{item.get('id')}/statuses?per_page=10",token)
            dep["statuses"]=[{"state":s.get("state"),"environment_url":s.get("environment_url"),"created_at":s.get("created_at"),"description":s.get("description")} for s in statuses]
        except Exception as exc: result["errors"].append({"source":"deployment_status","message":str(exc)[:200]})
        if created==day or any(date_of(st.get("created_at"))==day for st in dep["statuses"]):
            result["deployments"].append(dep)
    return result
def frontmatter(text):
    meta={}
    if not text.startswith("---"): return meta,text
    parts=text.split("---",2)
    if len(parts)<3: return meta,text
    for line in parts[1].splitlines():
        m=re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$",line)
        if m:
            value=m.group(2).strip().strip('"').strip("'")
            if value.startswith("[") and value.endswith("]"): value=[x.strip().strip('"').strip("'") for x in value[1:-1].split(",") if x.strip()]
            meta[m.group(1)]=value
    return meta,parts[2].strip()
def load_notes():
    notes={}
    for path in sorted((ROOT/"journal/daily").glob("**/*.md")):
        try: raw=path.read_text(encoding="utf-8")
        except OSError: continue
        meta,body=frontmatter(raw)
        m=re.search(r"(20\d{2}-\d{2}-\d{2})",path.name)
        date=meta.get("date") or (m.group(1) if m else None)
        try: day=dt.date.fromisoformat(str(date))
        except (ValueError,TypeError): continue
        notes[day.isoformat()]={"id":day.isoformat(),"date":day.isoformat(),"title":meta.get("title") or day.isoformat(),"category":meta.get("category","engineering"),"tags":meta.get("tags",[]),"status":meta.get("status","finalized"),"summary":meta.get("summary",""),"body":body,"source_path":str(path.relative_to(ROOT)),"source_hash":hashlib.sha256(raw.encode()).hexdigest()}
    return notes
def esc(value): return html.escape(str(value if value is not None else ""),quote=True)
def link(url,label):
    if not url or not str(url).startswith("https://"): return esc(label)
    return f'<a href="{esc(url)}" rel="noopener noreferrer">{esc(label)}</a>'
def svg_bars(counter,title):
    items=list(counter.items())[:12]
    if not items: return '<p class="muted">本周期没有可用的 GitHub 活动数据。</p>'
    maxv=max(v for _,v in items) or 1; rows=[]
    for i,(name,value) in enumerate(items):
        y=30+i*34; width=420*value/maxv
        rows.append(f'<text x="8" y="{y+14}" class="bar-label">{esc(name[:24])}</text><rect x="190" y="{y}" width="{width:.1f}" height="20" rx="5" class="bar"/><text x="{min(620,198+width):.1f}" y="{y+15}" class="bar-value">{value}</text>')
    height=max(70,len(rows)*34+12)
    return f'<svg viewBox="0 0 660 {height}" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title><desc>各仓库在报告周期内的提交数量。</desc>{"".join(rows)}</svg>'
def report_shell(title,subtitle,content,kind,root_prefix):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(title)}"><title>{esc(title)} · xm-journal</title><link rel="stylesheet" href="{root_prefix}assets/report.css"></head><body><header><a href="{root_prefix}index.html">← xm-journal</a><p class="eyebrow">{esc(kind.upper())} REPORT</p><h1>{esc(title)}</h1><p>{esc(subtitle)}</p></header><main>{content}</main><footer>xm-journal · Evidence first, reflection always.</footer></body></html>'''
def report_content(days, snapshots, notes, start, end, period_type, source_prefix='../../../'):
    days=[d.isoformat() if isinstance(d,dt.date) else str(d) for d in days]
    expected=(end-start).days+1; covered=[d for d in days if d in snapshots and not snapshots[d].get('note_only')]; note_days=[d for d in days if d in notes]
    commits=[]; prs=[]; runs=[]; deployments=[]; errors=[]; repo_counts=Counter(); active_repos=set()
    for d in covered:
        for repo in snapshots[d].get("repositories",[]):
            slug=repo.get("slug",repo.get("repository","?").split("/")[-1])
            repo_counts[slug]+=len(repo.get("commits",[])); 
            if any(repo.get(k) for k in ("commits","pull_requests","workflow_runs","deployments")): active_repos.add(slug)
            commits += [(slug,x) for x in repo.get("commits",[])]
            prs += [(slug,x) for x in repo.get("pull_requests",[])]
            runs += [(slug,x) for x in repo.get("workflow_runs",[])]
            deployments += [(slug,x) for x in repo.get("deployments",[])]
            errors += [(slug,x) for x in repo.get("errors",[])]
    complete=len(covered)==expected and end<=dt.datetime.now(TZ).date() and not errors
    status="最终版" if complete else "暂定 · 数据尚不完整"
    days_list=("".join(f'<li>{x}</li>' for x in covered) if period_type=="daily" else "".join(f'<li><a href="../../daily/{dt.date.fromisoformat(x).year}/{dt.date.fromisoformat(x).month:02d}/{x}.html">{x}</a></li>' for x in covered))
    missing=[(start+dt.timedelta(days=i)).isoformat() for i in range(expected) if (start+dt.timedelta(days=i)).isoformat() not in snapshots or snapshots[(start+dt.timedelta(days=i)).isoformat()].get("note_only")]
    kpis=[("记录覆盖",f"{len(covered)} / {expected} 天"),("有日志正文",f"{len(note_days)} 天"),("Git 提交",len(commits)),("PR 事件",len(prs)),("CI 运行",len(runs)),("部署事件",len(deployments))]
    kpi_html="".join(f'<article><span>{esc(k)}</span><strong>{esc(v)}</strong></article>' for k,v in kpis)
    summary=[]
    if commits: summary.append(f"周期内观察到 {len(commits)} 次提交，涉及 {len(active_repos)} 个仓库；提交数量代表活动，不直接等于成果价值。")
    if prs: summary.append(f"观察到 {len(prs)} 个 PR 创建、更新或合并事件；只有 merged 状态才计为已合并。")
    if deployments: summary.append(f"观察到 {len(deployments)} 个部署事件；只有部署状态为 success 才视为成功部署。")
    if not commits and not prs and not runs and not deployments: summary.append("本周期没有收集到 GitHub 活动事件；这不代表没有其他工作，需结合人工日报判断。")
    summary_html="".join(f"<li>{esc(s)}</li>" for s in summary)
    def event_rows(events,kind):
        if not events: return '<p class="muted">本周期暂无已采集事件。</p>'
        out=[]
        for slug,item in events[:25]:
            if kind=="commit": label=item.get("message","commit"); meta=item.get("sha","")
            elif kind=="pr": label=f"#{item.get('number')} {item.get('title')}"; meta=item.get("state","unknown")
            elif kind=="run": label=item.get("name","workflow"); meta=f"{item.get('status')} / {item.get('conclusion') or '未完成'}"
            else:
                sts=item.get("statuses",[]); state=sts[0].get("state") if sts else "无状态"
                label=f"{item.get('environment','environment')} deployment"; meta=state
            out.append(f'<li><b>{esc(slug)}</b> · {link(item.get("url"),label)} <small>{esc(meta)}</small></li>')
        if len(events)>25: out.append(f"<li class='muted'>仅展示最近 25 条；完整 {len(events)} 条原始事件保存在 data/github_activity 快照中。</li>")
        return "<ul class='events'>"+ "".join(out)+"</ul>"
    note_html=[]
    for d in note_days:
        n=notes[d]; note_html.append(f'<article class="note"><h3>{esc(n["title"])}</h3><p>{esc(n.get("summary") or "未填写摘要")}</p><div class="note-body">{esc(n.get("body", "")[:2400])}</div><a href="{source_prefix}{esc(n["source_path"])}">查看原始日志</a></article>')
    coverage=f'<p>报告状态：<b>{status}</b>。GitHub 快照覆盖 {len(covered)}/{expected} 天；人工日志覆盖 {len(note_days)} 天。两个覆盖率分开统计。</p>'
    if missing: coverage+=f'<p class="warning">缺少 GitHub 快照的日期：{esc(", ".join(missing))}</p>'
    if errors: coverage+=f'<p class="warning">采集异常 {len(errors)} 项；详情保存在每日活动 JSON 中，受限仓库或 API 失败不能当作零活动。</p>'
    chart_html=svg_bars(repo_counts,"各仓库提交数量")
    notes_html="".join(note_html) if note_html else "<p class='muted'>该周期尚未补充人工日志。GitHub 采集不能替代讨论背景、决策原因和主观复盘。</p>"
    return (coverage
      + f'<section><h2>关键观察</h2><ul>{summary_html}</ul></section>'
      + f'<section class="kpis">{kpi_html}</section>'
      + f'<section><h2>仓库活动分布</h2>{chart_html}<p class="muted">统计口径：提交数量；不衡量代码质量、用户价值或投入工时。</p></section>'
      + f'<section><h2>提交记录 · {len(commits)}</h2>{event_rows(commits,"commit")}</section>'
      + f'<section><h2>Pull Requests · {len(prs)}</h2>{event_rows(prs,"pr")}</section>'
      + f'<section><h2>CI 工作流 · {len(runs)}</h2>{event_rows(runs,"run")}</section>'
      + f'<section><h2>部署事件 · {len(deployments)}</h2>{event_rows(deployments,"deployment")}</section>'
      + f'<section><h2>人工日报与反思 · {len(note_days)}</h2>{notes_html}</section>'
      + f'<section><h2>数据覆盖日期</h2><ul>{days_list}</ul></section>')
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--date",help="Asia/Shanghai date YYYY-MM-DD; defaults to today")
    parser.add_argument("--skip-github",action="store_true")
    args=parser.parse_args()
    today=dt.date.fromisoformat(args.date) if args.date else dt.datetime.now(TZ).date()
    registry=read_json(ROOT/"config/projects.json",{"repositories":[]})
    snapshots_dir=ROOT/"data/github_activity"; snapshots_dir.mkdir(parents=True,exist_ok=True)
    snapshot_path=snapshots_dir/f"{today.isoformat()}.json"
    if not args.skip_github:
        token=os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        repos=[]
        for repo in registry["repositories"]:
            repos.append(collect_repo(repo,today,token))
            time.sleep(.15)
        snapshot={"date":today.isoformat(),"timezone":"Asia/Shanghai","collected_at":dt.datetime.now(TZ).isoformat(),"repositories":repos}
        write_json(snapshot_path,snapshot)
        print(f"Collected {len(repos)} repositories -> {snapshot_path.relative_to(ROOT)}")
    notes=load_notes()
    entries={"version":1,"entries":[{k:v for k,v in n.items() if k!="body"} for _,n in sorted(notes.items())]}
    write_json(ROOT/"data/entries.json",entries)
    all_snapshots={}
    for path in sorted(snapshots_dir.glob("20??-??-??.json")):
        snap=read_json(path,{})
        if snap.get("date"): all_snapshots[snap["date"]]=snap
    for d,n in notes.items():
        if d not in all_snapshots: all_snapshots[d]={"date":d,"repositories":[],"note_only":True}
    reports=[]
    for d,snap in sorted(all_snapshots.items()):
        day=dt.date.fromisoformat(d); n=notes.get(d)
        daily_content=report_content([day],all_snapshots,notes,day,day,"daily","../../../../")
        title=(n.get("title") if n else "GitHub 项目活动日报")
        subtitle=f"{d} · Asia/Shanghai · "+("已包含人工日志" if n else "GitHub 证据快照；人工日志待补充")
        rel=Path("reports/daily")/str(day.year)/f"{day.month:02d}"/f"{d}.html"
        (ROOT/rel).parent.mkdir(parents=True,exist_ok=True)
        (ROOT/rel).write_text(report_shell(title,subtitle,daily_content,"daily","../../../../"),encoding="utf-8")
        reports.append({"date":d,"path":rel.as_posix(),"type":"daily","has_note":bool(n),"snapshot":not snap.get("note_only")})
    periods=set()
    for d in all_snapshots:
        day=dt.date.fromisoformat(d)
        iso=day.isocalendar(); periods.add(("weekly",iso.year,iso.week))
        periods.add(("monthly",day.year,day.month))
    for typ,year,num in sorted(periods):
        if typ=="weekly":
            start=dt.date.fromisocalendar(year,num,1); end=start+dt.timedelta(days=6); name=f"{year}-W{num:02d}"; rel=Path("reports/weekly")/str(year)/f"weekly-{name}.html"
        else:
            start=dt.date(year,num,1); end=dt.date(year,num,calendar.monthrange(year,num)[1]); name=f"{year}-{num:02d}"; rel=Path("reports/monthly")/str(year)/f"monthly-{name}.html"
        if start>today: continue
        period_days=[start+dt.timedelta(days=i) for i in range((min(end,today)-start).days+1)]
        content=report_content(period_days,all_snapshots,notes,start,end,typ)
        subtitle=f"{start.isoformat()} 至 {end.isoformat()} · Asia/Shanghai · 自动汇总"
        (ROOT/rel).parent.mkdir(parents=True,exist_ok=True)
        (ROOT/rel).write_text(report_shell(("周度复盘 " if typ=="weekly" else "月度汇报 ")+name,subtitle,content,typ,"../../../"),encoding="utf-8")
        reports.append({"period":name,"start":start.isoformat(),"end":end.isoformat(),"path":rel.as_posix(),"type":typ})
    index={"version":1,"generated_at":dt.datetime.now(TZ).isoformat(),"timezone":"Asia/Shanghai","daily":[r for r in reports if r["type"]=="daily"],"weekly":[r for r in reports if r["type"]=="weekly"],"monthly":[r for r in reports if r["type"]=="monthly"]}
    write_json(ROOT/"reports/index.json",index)
    write_json(ROOT/"data/latest-activity.json",read_json(snapshot_path,{"date":today.isoformat(),"repositories":[]}))
    print(f"Generated {len(index['daily'])} daily, {len(index['weekly'])} weekly and {len(index['monthly'])} monthly reports.")
if __name__=="__main__": main()
