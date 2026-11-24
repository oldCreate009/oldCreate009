// Dashboard simples: os dados vêm de "dados-painel.js", criado pelo ETL.
// Para trocar títulos ou cores, edite index.html e styles.css.
const base = window.DADOS_PAINEL;
const cores = {Dengue:'#245a75', Zika:'#e39b42', Chikungunya:'#5b9b78'};
const formatar = n => new Intl.NumberFormat('pt-BR',{maximumFractionDigits:0}).format(n);
const decimal = n => new Intl.NumberFormat('pt-BR',{maximumFractionDigits:1}).format(n);
const el = id => document.getElementById(id);
const somar = (linhas,campo) => linhas.reduce((s,r)=>s+Number(r[campo]||0),0);

for(const bairro of base.bairros){
  const opcao=document.createElement('option');
  opcao.value=bairro.id; opcao.textContent=bairro.nome;
  el('bairro').appendChild(opcao);
}

// Cada botão exibe uma das três páginas.
document.querySelectorAll('.aba').forEach(botao=>botao.addEventListener('click',()=>{
  document.querySelectorAll('.aba').forEach(b=>b.classList.toggle('ativa',b===botao));
  document.querySelectorAll('.pagina').forEach(p=>p.classList.toggle('ativa',p.id===botao.dataset.aba));
  atualizar();
}));
['ano','doenca','bairro'].forEach(id=>el(id).addEventListener('change',atualizar));
el('limpar').addEventListener('click',()=>{
  ['ano','doenca','bairro'].forEach(id=>el(id).value='todos');
  atualizar();
});

function selecionar(tabela){
  const ano=el('ano').value, doenca=el('doenca').value, bairro=el('bairro').value;
  return tabela.filter(r=>
    (ano==='todos' || (r.mes||r.semana).slice(0,4)===ano) &&
    (bairro==='todos' || r.bairro===bairro) &&
    (!('doenca' in r) || doenca==='todos' || r.doenca===doenca));
}

function taxa(casos,bairro){
  const p=base.bairros.find(b=>b.id===bairro);
  return p ? casos / p.populacao * 100000 : 0;
}

// Gráfico de barras horizontais feito com HTML normal.
function barras(id,linhas){
  const caixa=el(id); caixa.replaceChildren();
  const max=Math.max(1,...linhas.map(r=>r.valor));
  for(const r of linhas){
    const row=document.createElement('div'); row.className='barra-linha';
    const nome=document.createElement('span'); nome.textContent=r.nome;
    const trilha=document.createElement('div'); trilha.className='trilha';
    const preenchimento=document.createElement('div'); preenchimento.className='preenchimento';
    preenchimento.style.width=(100*r.valor/max)+'%';
    if(r.cor) preenchimento.style.background=r.cor;
    trilha.appendChild(preenchimento);
    const numero=document.createElement('span'); numero.className='numero'; numero.textContent=r.texto||formatar(r.valor);
    row.append(nome,trilha,numero); caixa.appendChild(row);
  }
}

// SVG de linhas; não exige biblioteca externa nem internet.
function linhas(id,rotulos,series){
  const svg=el(id); svg.replaceChildren();
  if(!rotulos.length){svg.setAttribute('viewBox','0 0 800 250'); svg.innerHTML='<text x="20" y="40">Sem dados para este filtro.</text>';return;}
  const W=840,H=280,L=55,R=20,T=20,B=46;
  const valores=series.flatMap(s=>s.valores);
  const max=Math.max(1,...valores)*1.08;
  const x=i=>L+(W-L-R)*i/Math.max(1,rotulos.length-1);
  const y=v=>H-B-(H-T-B)*v/max;
  const ns='http://www.w3.org/2000/svg';
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
  function add(tag,attrs,txt){
    const n=document.createElementNS(ns,tag);
    for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);
    if(txt!==undefined)n.textContent=txt;
    svg.appendChild(n); return n;
  }
  for(let i=0;i<=4;i++){
    let v=max*i/4;
    add('line',{x1:L,y1:y(v),x2:W-R,y2:y(v),stroke:'#e1e8ec'});
    add('text',{x:L-8,y:y(v)+4,'text-anchor':'end','font-size':11,fill:'#6a7c87'},formatar(v));
  }
  const passo=Math.max(1,Math.ceil(rotulos.length/7));
  rotulos.forEach((r,i)=>{
    if(i%passo===0||i===rotulos.length-1)
      add('text',{x:x(i),y:H-20,'text-anchor':'middle','font-size':11,fill:'#6a7c87'},r);
  });
  for(const s of series){
    const pts=s.valores.map((v,i)=>x(i)+','+y(v)).join(' ');
    add('polyline',{points:pts,fill:'none',stroke:s.cor,'stroke-width':2.7,'stroke-linejoin':'round'});
    s.valores.forEach((v,i)=>{
      const ponto=add('circle',{cx:x(i),cy:y(v),r:3.5,fill:s.cor});
      const titulo=document.createElementNS(ns,'title');
      titulo.textContent=`${s.nome} | ${rotulos[i]}: ${decimal(v)}`;
      ponto.appendChild(titulo);
    });
  }
}

function visaoGeral(){
  const casos=selecionar(base.casos);
  // Controle vetorial: não filtrar por doença (mesmo foco pode afetar as três).
  const controle=selecionar(base.controle);
  const total=somar(casos,'total');
  const moradores=base.bairros.filter(b=>el('bairro').value==='todos'||b.id===el('bairro').value);
  const populacao=somar(moradores,'populacao');
  el('total-casos').textContent=formatar(total);
  el('total-focos').textContent=formatar(somar(controle,'focos'));
  el('total-visitas').textContent=formatar(somar(controle,'visitas'));
  el('total-taxa').textContent=decimal(populacao?total/populacao*100000:0);

  const meses=[...new Set(casos.map(r=>r.mes))].sort();
  const doencas=el('doenca').value==='todos'?Object.keys(cores):[el('doenca').value];
  const series=doencas.map(d=>({nome:d,cor:cores[d],valores:meses.map(m=>somar(casos.filter(r=>r.mes===m&&r.doenca===d),'total'))}));
  linhas('grafico-meses',meses,series);
  el('legenda-meses').replaceChildren();
  for(const s of series){
    const span=document.createElement('span');
    const mark=document.createElement('i');mark.className='bolinha';mark.style.background=s.cor;
    span.append(mark,document.createTextNode(s.nome));el('legenda-meses').appendChild(span);
  }
  barras('barras-doencas',doencas.map(d=>({nome:d,valor:somar(casos.filter(r=>r.doenca===d),'total'),cor:cores[d]})));
}

function visaoBairros(){
  const casos=selecionar(base.casos), controle=selecionar(base.controle);
  const selecionados=base.bairros.filter(b=>el('bairro').value==='todos'||b.id===el('bairro').value);
  const lista=selecionados.map(b=>{
    const n=somar(casos.filter(c=>c.bairro===b.id),'total');
    const cont=controle.filter(c=>c.bairro===b.id);
    return {...b,casos:n,taxa:taxa(n,b.id),focos:somar(cont,'focos'),visitas:somar(cont,'visitas'),eliminados:somar(cont,'eliminados')};
  }).sort((a,b)=>b.taxa-a.taxa);
  barras('barras-bairros',lista.map(b=>({nome:b.nome,valor:b.taxa,texto:decimal(b.taxa)})));
  const tbody=el('tabela-bairros');tbody.replaceChildren();
  for(const r of lista){
    const tr=document.createElement('tr');
    for(const valor of [r.nome,formatar(r.casos),formatar(r.focos),formatar(r.visitas),formatar(r.eliminados)]){
      const td=document.createElement('td');td.textContent=valor;tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
  // Os pontos servem apenas como esquema interativo, NÃO como mapa municipal.
  const svg=el('mapa');svg.replaceChildren();svg.setAttribute('viewBox','0 0 440 265');
  const ns='http://www.w3.org/2000/svg';
  const criar=(tag,atr,valor)=>{
    const e=document.createElementNS(ns,tag);
    for(const [k,v] of Object.entries(atr))e.setAttribute(k,v);
    if(valor!==undefined)e.textContent=valor;
    svg.appendChild(e);return e;
  };
  criar('rect',{x:10,y:10,width:420,height:238,rx:6,fill:'#f1f6f9',stroke:'#c5d7e2'});
  const coords=base.bairros;
  const lat=coords.map(c=>c.lat),lon=coords.map(c=>c.lon);
  const n=(v,min,max)=>max===min ? 0.5 : (v-min)/(max-min);
  for(const b of coords){
    const x=52+335*n(b.lon,Math.min(...lon),Math.max(...lon));
    const y=38+180*(1-n(b.lat,Math.min(...lat),Math.max(...lat)));
    const ativo=el('bairro').value==='todos'||el('bairro').value===b.id;
    const g=criar('g',{'data-bairro':b.id,style:'cursor:pointer'});
    const ponto=document.createElementNS(ns,'circle');
    ponto.setAttribute('cx',x);ponto.setAttribute('cy',y);ponto.setAttribute('r',10);
    ponto.setAttribute('fill',ativo?'#245a75':'#bbc7ce');g.appendChild(ponto);
    const nome=document.createElementNS(ns,'text');
    nome.setAttribute('x',x);nome.setAttribute('y',y-15);
    nome.setAttribute('font-size','11');nome.setAttribute('text-anchor','middle');nome.textContent=b.nome.replace('Bairro ','');g.appendChild(nome);
    const titulo=document.createElementNS(ns,'title');titulo.textContent=`${b.nome}. Clique para selecionar.`;g.appendChild(titulo);
    g.addEventListener('click',()=>{el('bairro').value=b.id;atualizar();});
  }
}

function visaoModelo(){
  const previsoes=selecionar(base.previsoes);
  const msg=el('aviso-previsao');
  msg.textContent=previsoes.length?'Resultados obtidos exclusivamente no período de teste.':'';
  if(!previsoes.length){msg.textContent='Sem previsões neste recorte. Selecione o ano de 2025.';}
  const mae=previsoes.length?previsoes.reduce((s,r)=>s+Math.abs(r.real-r.previsto),0)/previsoes.length:0;
  const baseline=previsoes.length?previsoes.reduce((s,r)=>s+Math.abs(r.real-r.base),0)/previsoes.length:0;
  el('mae-modelo').textContent=previsoes.length?decimal(mae):'–';
  el('mae-base').textContent=previsoes.length?decimal(baseline):'–';
  const semanas=[...new Set(previsoes.map(r=>r.semana))].sort();
  linhas('grafico-previsao',semanas,[
    {nome:'Observado',cor:'#245a75',valores:semanas.map(s=>somar(previsoes.filter(r=>r.semana===s),'real'))},
    {nome:'Previsto',cor:'#e39b42',valores:semanas.map(s=>somar(previsoes.filter(r=>r.semana===s),'previsto'))},
  ]);
}

function atualizar(){visaoGeral();visaoBairros();visaoModelo();}
atualizar();
