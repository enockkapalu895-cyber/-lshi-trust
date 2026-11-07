<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pedals for Peace - Day 1 Goma</title>
<style>
  body{margin:0;background:#111;font-family:sans-serif;text-align:center;color:white;overflow:hidden}
  h1{font-size:18px;margin:8px 0 2px}
  p{font-size:13px;margin:2px}
  #game{width:100%;height:340px;background:linear-gradient(#87CEEB,#E8F5E9);position:relative;overflow:hidden;border-top:3px solid #222;border-bottom:3px solid #222}
  #road{position:absolute;bottom:0;width:100%;height:70px;background:#555}
  #line{position:absolute;bottom:35px;width:100%;border-top:3px dashed yellow}
  #bike{position:absolute;bottom:65px;left:40px;font-size:48px;transition:bottom .25s}
  .hole{position:absolute;bottom:55px;width:45px;height:25px;background:#111;border-radius:50%;font-size:10px;color:white;text-align:center}
  .msg{position:absolute;bottom:130px;font-size:32px}
  #hud{display:flex;justify-content:space-around;background:#222;padding:8px;font-size:14px}
  button{width:45%;padding:15px;font-size:18px;font-weight:bold;border-radius:12px;border:none;margin:8px 5px}
  #pedal{background:#FFD600}
  #jump{background:#00C853;color:white}
</style>
</head>
<body>
<h1>🚲 PEDALS FOR PEACE - Day 1 Goma</h1>
<p>Un seul vélo, un seul message : la paix à l'est de la RDC</p>
<div id="hud">
  <span>❤️ Énergie: <b id="energy">100</b></span>
  <span>✉️ Messages: <b id="score">0</b>/5</span>
  <span>📍 <b id="dist">0</b> m</span>
</div>
<div id="game">
  <div id="road"></div><div id="line"></div>
  <div id="bike">🚴🏿‍♂️</div>
</div>
<button id="pedal">PÉDALER 🚲</button>
<button id="jump">SAUTER ⬆️</button>
<p id="info">Appuie sur PÉDALER pour avancer. Évite les trous noirs, ramasse les ✉️</p>

<script>
let energy=100, score=0, dist=0, bikeY=65, jumping=false;
let bike=document.getElementById('bike');
let game=document.getElementById('game');

function update(){ document.getElementById('energy').innerText=energy; document.getElementById('score').innerText=score; document.getElementById('dist').innerText=dist; }

document.getElementById('pedal').onclick=()=>{
  if(energy<=0){ alert('Tu es fatigué ! Repose-toi... Mais Miguel n’abandonnait pas. Recommence Day 1'); location.reload(); return; }
  energy-=2; dist+=20; update();
  bike.style.left = Math.min(280, 40+dist/5)+'px';
  if(dist>=500 && score>=5){ alert('BRAVO ! Day 1 terminé ! Goma -> Sake. Tu as porté le message de Miguel. Demain Day 2 !'); location.reload(); }
  if(dist>=500 && score<5){ alert('Tu es arrivé mais tu as oublié des messages de paix. Recommence pour ramasser les 5 ✉️'); location.reload(); }
};

document.getElementById('jump').onclick=()=>{
  if(jumping) return; jumping=true; bike.style.bottom='140px';
  setTimeout(()=>{ bike.style.bottom='65px'; jumping=false; },400);
};

// Créer trous et messages
setInterval(()=>{
  if(Math.random()<0.6){
    let h=document.createElement('div'); h.className='hole'; h.innerText='TROU'; h.style.left='100%'; game.appendChild(h);
    let move=setInterval(()=>{ let l=parseInt(h.style.left); if(isNaN(l)) l=window.innerWidth; l-=8; h.style.left=l+'px';
      let bikePos=parseInt(bike.style.left)||40;
      if(l>bikePos-20 && l<bikePos+40 && !jumping){ alert('Ouch ! Tu es tombé dans un trou à Goma. Miguel se relevait toujours. Recommence.'); location.reload(); }
      if(l<-50){ clearInterval(move); h.remove(); }
    },40);
  } else {
    let m=document.createElement('div'); m.className='msg'; m.innerText='✉️'; m.style.left='100%'; game.appendChild(m);
    let move=setInterval(()=>{ let l=parseInt(m.style.left); if(isNaN(l)) l=window.innerWidth; l-=5; m.style.left=l+'px';
      let bikePos=parseInt(bike.style.left)||40;
      if(l>bikePos-10 && l<bikePos+50){ score++; update(); m.remove(); clearInterval(move); }
      if(l<-50){ clearInterval(move); m.remove(); }
    },40);
  }
},1800);
update();
</script>
</body>
</html>
