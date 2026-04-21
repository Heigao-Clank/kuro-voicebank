(function(){
  var sidebarToggle=document.getElementById('sidebarToggle');
  var sidebar=document.getElementById('sidebar');
  var sidebarOverlay=document.getElementById('sidebarOverlay');
  var langSwitcher=document.querySelector('.lang-switcher');

  function openSidebar(){
    sidebar.classList.add('open');
    sidebarToggle.classList.add('active');
    sidebarOverlay.classList.add('active');
    if(langSwitcher)langSwitcher.classList.add('hidden');
    document.body.style.overflow='hidden';
  }
  function closeSidebar(){
    sidebar.classList.remove('open');
    sidebarToggle.classList.remove('active');
    sidebarOverlay.classList.remove('active');
    if(langSwitcher)langSwitcher.classList.remove('hidden');
    document.body.style.overflow='';
  }

  sidebarToggle.addEventListener('click',function(){
    if(sidebar.classList.contains('open')){closeSidebar();}else{openSidebar();}
  });
  sidebarOverlay.addEventListener('click',closeSidebar);

  sidebar.querySelectorAll('a').forEach(function(link){
    link.addEventListener('click',function(){
      if(window.innerWidth<=900)closeSidebar();
    });
  });

  var navLinks=sidebar.querySelectorAll('.sidebar-nav a');
  var sections=document.querySelectorAll('section[id]');

  function highlightNav(){
    var current='';
    var scrollPosition=window.scrollY+window.innerHeight/2;
    sections.forEach(function(section){
      var rect=section.getBoundingClientRect();
      var sectionTop=rect.top+window.scrollY;
      var sectionBottom=sectionTop+rect.height;
      if(scrollPosition>=sectionTop&&scrollPosition<sectionBottom){
        current=section.getAttribute('id');
      }
    });
    if(window.scrollY<100)current='hero';
    if(!current&&sections.length>0){
      var lastSection=sections[sections.length-1];
      var lastRect=lastSection.getBoundingClientRect();
      var lastSectionTop=lastRect.top+window.scrollY;
      if(window.scrollY>=lastSectionTop)current=lastSection.getAttribute('id');
    }
    navLinks.forEach(function(link){
      link.classList.remove('active');
      if(link.getAttribute('href')==='#'+current)link.classList.add('active');
    });
  }

  var _scrollT;
  window.addEventListener('scroll',function(){
    if(_scrollT)return;
    _scrollT=requestAnimationFrame(function(){_scrollT=null;highlightNav();});
  });
  highlightNav();

  navLinks.forEach(function(link){
    link.addEventListener('click',function(){
      navLinks.forEach(function(l){l.classList.remove('active');});
      this.classList.add('active');
    });
  });

  window.toggleAccordion=function(element){
    var accordion=element.parentElement;
    var isActive=accordion.classList.toggle('active');
    element.setAttribute('aria-expanded',isActive);
  };

  window.toggleFaq=function(element){
    var faqItem=element.parentElement;
    var isActive=faqItem.classList.toggle('active');
    element.setAttribute('aria-expanded',isActive);
  };

  document.querySelectorAll('.protocol-tab').forEach(function(tab){
    tab.addEventListener('click',function(){
      var lang=this.getAttribute('data-lang');
      document.querySelectorAll('.protocol-tab').forEach(function(t){t.classList.remove('active');});
      document.querySelectorAll('.protocol-content').forEach(function(c){c.style.display='none';});
      this.classList.add('active');
      var el=document.getElementById('protocol-'+lang);
      if(el&&!el.innerHTML.trim()){
        el.innerHTML='<div class="protocol-text">'+(window._protocolData||{})[lang]+'</div>';
      }
      el.style.display='block';
    });
  });

  function formatTime(seconds){
    var mins=Math.floor(seconds/60);
    var secs=Math.floor(seconds%60);
    return mins+':'+(secs<10?'0':'')+secs;
  }

  var activePlayerIndex=-1;

  function lerp(a,b,t){return a+(b-a)*t;}

  function smoothNoise(t,seed){
    var i=Math.floor(t);
    var f=t-i;
    f=f*f*(3-2*f);
    return lerp(hash(i+seed),hash(i+1+seed),f);
  }
  function hash(n){
    var s=Math.sin(n*127.1+n*311.7)*43758.5453;
    return s-Math.floor(s);
  }

  function drawBars(canvas,smooth){
    var c=canvas.getContext('2d');
    var w=canvas.width;
    var h=canvas.height;
    c.clearRect(0,0,w,h);
    var barCount=64;
    var barW=Math.max(1,(w/barCount)*0.55);
    var gap=(w-barW*barCount)/(barCount+1);
    for(var i=0;i<barCount;i++){
      var x=gap+(barW+gap)*i;
      var v=smooth[i];
      var barH=Math.max(2,v*h*0.78);
      var y=(h-barH)/2;
      var r=barW/2;

      c.shadowColor='rgba(100,150,200,'+(v*0.25)+')';
      c.shadowBlur=v*6;

      var grad=c.createLinearGradient(0,y,0,y+barH);
      grad.addColorStop(0,'rgba(130,170,220,'+(0.15+v*0.55)+')');
      grad.addColorStop(0.5,'rgba(110,155,210,'+(0.1+v*0.65)+')');
      grad.addColorStop(1,'rgba(90,135,195,'+(0.15+v*0.55)+')');
      c.fillStyle=grad;

      c.beginPath();
      c.moveTo(x+r,y);
      c.lineTo(x+barW-r,y);
      c.quadraticCurveTo(x+barW,y,x+barW,y+r);
      c.lineTo(x+barW,y+barH-r);
      c.quadraticCurveTo(x+barW,y+barH,x+barW-r,y+barH);
      c.lineTo(x+r,y+barH);
      c.quadraticCurveTo(x,y+barH,x,y+barH-r);
      c.lineTo(x,y+r);
      c.quadraticCurveTo(x,y,x+r,y);
      c.fill();
    }
    c.shadowBlur=0;
  }

  var players=document.querySelectorAll('.demo-card');
  players.forEach(function(player){
    var audio=player.querySelector('audio');
    var canvas=player.querySelector('.demo-canvas');
    var playBtn=player.querySelector('.demo-play-btn');
    var progressEl=player.querySelector('.demo-progress');
    var progressBar=player.querySelector('.demo-progress-bar');
    var timeEl=player.querySelector('.demo-time');
    var iconPlay=playBtn.querySelector('.icon-play');
    var iconPause=playBtn.querySelector('.icon-pause');
    var source=audio?audio.querySelector('source'):null;
    var index=parseInt(player.getAttribute('data-index'));
    var currentEnergy=0.08;
    var seeking=false;
    var barState=new Array(64);
    for(var k=0;k<64;k++)barState[k]=0.05;
    var rafId=null;

    function resizeCanvas(){
      var rect=canvas.parentElement.getBoundingClientRect();
      canvas.width=rect.width*window.devicePixelRatio;
      canvas.height=rect.height*window.devicePixelRatio;
    }
    resizeCanvas();
    window.addEventListener('resize',resizeCanvas);

    if(!source||!source.src){
      playBtn.style.opacity='0.3';
      playBtn.style.pointerEvents='none';
      if(rafId)cancelAnimationFrame(rafId);
      return;
    }

    function pauseOthers(){
      if(activePlayerIndex>=0&&activePlayerIndex!==index){
        var prev=players[activePlayerIndex];
        if(prev){
          prev.querySelector('audio').pause();
          prev.querySelector('.icon-play').style.display='block';
          prev.querySelector('.icon-pause').style.display='none';
        }
      }
    }

    function tick(){
      var playing=activePlayerIndex===index&&!audio.paused;
      var target=playing?0.75:0.08;
      currentEnergy=lerp(currentEnergy,target,0.045);

      var t=Date.now()/1000;
      var smooth=[];
      for(var i=0;i<64;i++){
        var di=Math.abs(i-31.5)/31.5;
        var envelope=Math.exp(-di*di*1.8);
        var n1=smoothNoise(t*1.8+i*0.08,index*99);
        var n2=smoothNoise(t*3.6+i*0.15,index*99+50);
        var n3=smoothNoise(t*0.6+i*0.04,index*99+100);
        var wave=(n1*0.45+n2*0.35+n3*0.2)*envelope;
        var barTarget=wave*currentEnergy;
        barState[i]=lerp(barState[i],barTarget,0.12);
        smooth.push(barState[i]);
      }
      drawBars(canvas,smooth);

      var delay=currentEnergy<0.15?80:0;
      if(delay>0){
        setTimeout(function(){rafId=requestAnimationFrame(tick);},delay);
      }else{
        rafId=requestAnimationFrame(tick);
      }
    }
    rafId=requestAnimationFrame(tick);

    playBtn.addEventListener('click',function(){
      if(activePlayerIndex===index&&!audio.paused){
        audio.pause();
        iconPlay.style.display='block';
        iconPause.style.display='none';
        activePlayerIndex=-1;
        return;
      }
      pauseOthers();
      activePlayerIndex=index;
      audio.play().then(function(){
        iconPlay.style.display='none';
        iconPause.style.display='block';
      }).catch(function(){
        iconPlay.style.display='block';
        iconPause.style.display='none';
      });
    });

    audio.addEventListener('timeupdate',function(){
      if(seeking)return;
      var pct=(audio.currentTime/audio.duration)*100;
      progressBar.style.width=pct+'%';
      timeEl.textContent=formatTime(audio.currentTime)+' / '+formatTime(audio.duration);
    });

    function seekFromEvent(e){
      var rect=progressEl.getBoundingClientRect();
      var x=Math.max(0,Math.min(e.clientX-rect.left,rect.width));
      var pct=x/rect.width;
      if(audio.duration){
        audio.currentTime=pct*audio.duration;
        progressBar.style.width=(pct*100)+'%';
        timeEl.textContent=formatTime(audio.currentTime)+' / '+formatTime(audio.duration);
      }
    }

    progressEl.addEventListener('mousedown',function(e){
      seeking=true;
      seekFromEvent(e);
      function onMove(ev){seekFromEvent(ev);}
      function onUp(){
        seeking=false;
        document.removeEventListener('mousemove',onMove);
        document.removeEventListener('mouseup',onUp);
      }
      document.addEventListener('mousemove',onMove);
      document.addEventListener('mouseup',onUp);
    });

    progressEl.addEventListener('touchstart',function(e){
      seeking=true;
      seekFromEvent(e.touches[0]);
    },{passive:true});

    document.addEventListener('touchmove',function(e){
      if(!seeking)return;
      seekFromEvent(e.touches[0]);
    },{passive:true});

    document.addEventListener('touchend',function(){
      seeking=false;
    });

    audio.addEventListener('loadedmetadata',function(){
      timeEl.textContent='0:00 / '+formatTime(audio.duration);
    });

    audio.addEventListener('ended',function(){
      iconPlay.style.display='block';
      iconPause.style.display='none';
      progressBar.style.width='0%';
      activePlayerIndex=-1;
    });
  });

  if('IntersectionObserver' in window){
    var animSections=document.querySelectorAll('section[id]');
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.remove('anim-paused');
        }else{
          entry.target.classList.add('anim-paused');
        }
      });
    },{rootMargin:'100px'});
    animSections.forEach(function(s){io.observe(s);});
  }
})();
