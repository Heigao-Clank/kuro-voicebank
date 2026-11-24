(function () {
  const pageLanguage = document.documentElement.lang;
  const ui = {
    'zh-CN': {play: '播放', failed: '试听加载失败，请点播放按钮重试。', retry: '重试播放', pause: '暂停', seek: '播放进度', copied: '已复制', manual: '请选择并复制命令'},
    en: {play: 'Play', failed: 'Audio could not be loaded. Press play to try again.', retry: 'Retry playback', pause: 'Pause', seek: 'Playback position', copied: 'Copied', manual: 'Select and copy the command'},
    ja: {play: '再生', failed: '試聴音声を読み込めませんでした。再生ボタンを押して、もう一度お試しください。', retry: '再生を再試行', pause: '一時停止', seek: '再生位置', copied: 'コピーしました', manual: 'コマンドを選択してコピーしてください'}
  }[pageLanguage];

  const header = document.querySelector('.topnav');
  const navigation = header.querySelector('.topnav-nav');
  const navLinks = navigation.querySelectorAll('.topnav-link');
  const languages = header.querySelectorAll('.topnav-lang a');
  const sections = Array.from(document.querySelectorAll('section[id]'));

  function revealActiveLink() {
    const link = navigation.querySelector('[aria-current="location"]');
    if (!link || navigation.scrollWidth <= navigation.clientWidth) return;
    const menu = navigation.getBoundingClientRect();
    const item = link.getBoundingClientRect();
    if (item.left < menu.left) navigation.scrollLeft += item.left - menu.left - 4;
    else if (item.right > menu.right) navigation.scrollLeft += item.right - menu.right + 4;
  }

  let highlightedSection;
  function highlightNav() {
    const anchor = header.getBoundingClientRect().height + 16;
    let current = sections[0].id;
    for (const section of sections) {
      if (section.getBoundingClientRect().top > anchor) break;
      current = section.id;
    }
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
      current = sections[sections.length - 1].id;
    }
    navLinks.forEach(link => {
      const active = link.hash === '#' + current;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    languages.forEach(link => { link.hash = current === 'hero' ? '' : current; });
    if (current !== highlightedSection) {
      highlightedSection = current;
      revealActiveLink();
    }
  }
  let pending = false;
  function scheduleHighlight() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; highlightNav(); });
  }
  window.addEventListener('scroll', scheduleHighlight, {passive: true});
  window.addEventListener('resize', () => {
    scheduleHighlight();
    revealActiveLink();
  });
  document.fonts.ready.then(revealActiveLink);
  window.addEventListener('pageshow', scheduleHighlight);
  highlightNav();

  const tabs = document.querySelectorAll('.protocol-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(button => {
        const selected = button === tab;
        button.classList.toggle('active', selected);
        button.setAttribute('aria-pressed', String(selected));
        document.getElementById(button.getAttribute('aria-controls')).hidden = !selected;
      });
    });
  });

  const copy = document.querySelector('.install-copy');
  const command = document.querySelector('.install-command code');
  const status = document.querySelector('.copy-status');
  copy.hidden = false;
  const copyLabel = copy.title;
  let feedbackTimer;
  copy.addEventListener('click', async () => {
    let copied = false;
    try {
      await navigator.clipboard.writeText(command.textContent);
      copied = true;
    } catch {
      const range = document.createRange();
      range.selectNodeContents(command);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      try { copied = document.execCommand('copy'); } catch { /* Keep the command selected for manual copying. */ }
      if (copied) selection.removeAllRanges();
    }
    clearTimeout(feedbackTimer);
    status.textContent = copied ? ui.copied : ui.manual;
    copy.classList.toggle('copied', copied);
    copy.title = status.textContent;
    feedbackTimer = setTimeout(() => {
      copy.classList.remove('copied');
      copy.title = copyLabel;
      status.textContent = '';
    }, 2500);
  });

  function formatTime(seconds) {
    return Math.floor(seconds / 60) + ':' + String(Math.floor(seconds % 60)).padStart(2, '0');
  }

  var players = document.querySelectorAll('.demo-card');
  players.forEach(function (card) {
    var audio = card.querySelector('audio');
    var playButton = card.querySelector('.demo-play-btn');
    var slider = card.querySelector('.demo-progress');
    var progressBar = slider.querySelector('.demo-progress-bar');
    var timeLabel = card.querySelector('.demo-time');
    var playIcon = playButton.querySelector('.icon-play');
    var pauseIcon = playButton.querySelector('.icon-pause');
    var title = card.querySelector('.demo-card-desc').textContent.trim();
    const message = card.querySelector('.demo-status');
    let failed = false;
    let playRequest = 0;
    slider.setAttribute('role', 'slider');
    slider.tabIndex = 0;
    slider.setAttribute('aria-label', ui.seek + ' · ' + title);
    slider.setAttribute('aria-valuemin', '0');

    function duration() {
      // A locally opened Ogg file can report Infinity until its last page is read.
      return Number.isFinite(audio.duration) && audio.duration > 0
        ? audio.duration : Number(audio.dataset.duration);
    }

    function renderProgress() {
      var length = duration();
      var position = audio.ended ? length : Math.min(audio.currentTime, length);
      var percent = Math.min(100, position / length * 100) + '%';
      card.style.setProperty('--played', percent);
      progressBar.style.width = percent;
      timeLabel.textContent = formatTime(position) + ' / ' + formatTime(length);
      slider.setAttribute('aria-valuemax', String(Math.floor(length)));
      slider.setAttribute('aria-valuenow', String(Math.floor(position)));
      slider.setAttribute('aria-valuetext', timeLabel.textContent);
    }

    function renderButton() {
      const playing = !failed && !audio.paused && !audio.ended;
      playIcon.style.display = playing ? 'none' : 'block';
      pauseIcon.style.display = playing ? 'block' : 'none';
      const label = failed ? ui.retry : (playing ? ui.pause : ui.play);
      playButton.setAttribute('aria-label', label + ' · ' + title);
    }

    function showFailure() {
      if (failed) return;
      failed = true;
      playRequest++;
      audio.pause();
      message.textContent = ui.failed;
      renderButton();
    }

    // Source errors do not bubble. Let the browser try MP3 if Opus fails.
    audio.querySelector('source:last-of-type').addEventListener('error', showFailure);
    audio.addEventListener('error', showFailure);
    playButton.addEventListener('click', function () {
      if (failed) {
        failed = false;
        message.textContent = '';
        audio.load();
      } else if (audio.ended) {
        audio.currentTime = 0;
      } else if (!audio.paused) {
        audio.pause();
        return;
      }
      const request = ++playRequest;
      audio.play().catch(error => {
        if (request === playRequest && error.name !== 'AbortError') showFailure();
      });
    });
    audio.addEventListener('play', function () {
      players.forEach(function (other) {
        if (other !== card) other.querySelector('audio').pause();
      });
      renderButton();
    });
    audio.addEventListener('pause', renderButton);
    audio.addEventListener('ended', renderButton);
    ['loadedmetadata', 'durationchange', 'timeupdate', 'seeked', 'ended'].forEach(function (event) {
      audio.addEventListener(event, renderProgress);
    });

    function seek(event) {
      var bounds = slider.getBoundingClientRect();
      var fraction = Math.max(0, Math.min(1, (event.clientX - bounds.left) / bounds.width));
      audio.currentTime = fraction * duration();
      renderProgress();
    }
    slider.addEventListener('pointerdown', function (event) {
      if (!event.isPrimary || event.button !== 0) return;
      slider.setPointerCapture(event.pointerId);
      seek(event);
    });
    slider.addEventListener('pointermove', function (event) {
      if (slider.hasPointerCapture(event.pointerId)) seek(event);
    });
    slider.addEventListener('keydown', function (event) {
      var target;
      switch (event.key) {
        case 'ArrowRight': case 'ArrowUp': target = audio.currentTime + 5; break;
        case 'ArrowLeft': case 'ArrowDown': target = audio.currentTime - 5; break;
        case 'Home': target = 0; break;
        case 'End': target = duration(); break;
        default: return;
      }
      event.preventDefault();
      audio.currentTime = Math.max(0, Math.min(duration(), target));
      renderProgress();
    });
    if (audio.error || audio.networkState === audio.NETWORK_NO_SOURCE) showFailure();
    renderButton();
    renderProgress();
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
