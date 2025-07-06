const API = "";

async function getStatus() {
  const r = await fetch(API + "/api/status");
  return await r.json();
}
async function getHistory() {
  const r = await fetch(API + "/api/history");
  return await r.json();
}
async function getActions() {
  const r = await fetch(API + "/api/actions");
  return await r.json();
}
function renderStatus(s) {
  document.getElementById("status").textContent =
    `Battery ${s.battery_voltage.toFixed(2)} V | Absorb ${s.absorb_voltage} V | Float ${s.float_voltage} V`;
  document.getElementById("absorb").value = s.absorb_voltage;
  document.getElementById("float").value = s.float_voltage;
}
function renderActions(actions) {
  const ul = document.getElementById("actionList");
  ul.innerHTML = "";
  actions.slice().reverse().forEach(a => {
    const li = document.createElement("li");
    li.className = "pb1";
    const date = new Date(a.ts * 1000).toLocaleTimeString();
    li.textContent = `${date} — ${a.action}`;
    ul.appendChild(li);
  });
}
async function drawGraph(hist) {
  const ctx = document.getElementById("vgraph").getContext("2d");
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: hist.map(p => new Date(p.t*1000).toLocaleTimeString()),
      datasets: [{
        label: "Voltage",
        data: hist.map(p => p.v),
        tension: 0.2,
        fill: false
      }]
    },
    options: { responsive: true, scales: {y: {beginAtZero:false}} }
  });
}
async function refresh() {
  const [s,h,a] = await Promise.all([getStatus(), getHistory(), getActions()]);
  renderStatus(s);
  renderActions(a);
  drawGraph(h);
}
document.getElementById("setbtn").addEventListener("click", async ()=>{
  const absorb=parseFloat(document.getElementById("absorb").value);
  const flt=parseFloat(document.getElementById("float").value);
  await fetch(API + "/api/setpoints",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({absorb:absorb,float:flt})
  });
  refresh();
});
refresh();
setInterval(refresh, 30000);
