function copyIP() {

const ip = document.getElementById("ip").innerText;

navigator.clipboard.writeText(ip);

alert("IPをコピーしました！");
}



async function loadServerStatus(){

try{

const res = await fetch("https://api.mcsrvstat.us/bedrock/2/05.jpn.gg");

const data = await res.json();

if(data.players){

document.getElementById("players").innerText =
data.players.online + " / " + data.players.max;

}else{

document.getElementById("players").innerText = "取得できません";

}

}catch{

document.getElementById("players").innerText = "オフライン";

}

}

loadServerStatus();

setInterval(loadServerStatus,30000);
