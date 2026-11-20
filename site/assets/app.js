async function loadJson(path){const r=await fetch(path);if(!r.ok)throw new Error(path+" "+r.status);return r.json()}
function el(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n}
function addLink(parent,url,label){const a=el("a","",label);a.href=url;parent.append(a)}
async function main(){
 const [projects,activity,index]=await Promise.all([loadJson("config/projects.json"),loadJson("data/latest-activity.json"),loadJson("reports/index.json")]);
 const repos=activity.repositories||[];const commits=repos.reduce((n,r)=>n+(r.commits||[]).length,0);const deployments=repos.reduce((n,r)=>n+(r.deployments||[]).length,0);
 document.querySelector("#project-count").textContent=projects.repositories.length;document.querySelector("#commit-count").textContent=commits;document.querySelector("#deploy-count").textContent=deployments;
 const projectRoot=document.querySelector("#project-list");projectRoot.replaceChildren();
 for(const p of projects.repositories){const r=repos.find(x=>x.slug===p.slug);const card=el("article","project-card");card.append(el("h3","",p.display_name),el("p","",p.description));card.append(el("p","muted",r?("提交 "+(r.commits||[]).length+" · PR "+(r.pull_requests||[]).length+" · CI "+(r.workflow_runs||[]).length+" · 部署 "+(r.deployments||[]).length):"本日快照缺失"));addLink(card,"https://github.com/"+p.full_name,"打开仓库");if(r&&r.errors&&r.errors.length)card.append(el("p","warning","部分 GitHub API 数据不可用"));projectRoot.append(card)}
 for(const [key,id,label] of [["daily","#daily-list","日报"],["weekly","#weekly-list","周报"],["monthly","#monthly-list","月报"]]){const root=document.querySelector(id);root.replaceChildren();const items=(index[key]||[]).slice().reverse();if(!items.length){root.append(el("p","empty","暂无"+label));continue}for(const item of items.slice(0,12)){const row=el("article","report-item");row.append(el("strong","",item.date||item.period));if(item.has_note===false)row.append(el("span","muted"," · 待补充人工日志"));addLink(row,item.path,"打开报告");root.append(row)}}
}
main().catch(error=>{for(const id of ["#project-list","#daily-list","#weekly-list","#monthly-list"]){const n=document.querySelector(id);if(n)n.textContent="数据加载失败："+error.message}});
