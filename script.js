function copyIP(){

navigator.clipboard.writeText("05.jpn.gg");

alert("IPをコピーしました");

}



async function loadServerStatus(){

try{

const res = await fetch("https://api.mcsrvstat.us/bedrock/2/05.jpn.gg");

const data = await res.json();

if(data.players){

document.getElementById("players").innerText =
data.players.online + " / " + data.players.max;

}

}catch{

document.getElementById("players").innerText="取得できません";

}

}

loadServerStatus();

setInterval(loadServerStatus,30000);
