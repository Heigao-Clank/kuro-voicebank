(() => {
  const menu = document.querySelector('.catalog-languages');
  const sections = document.querySelector('.catalog-sections');
  const sectionButtons = document.querySelectorAll('[data-section]');
  const localizedLinks = document.querySelectorAll('[data-local-link]');
  const fields = document.querySelectorAll('[data-copy]');
  const description = document.querySelector('meta[name="description"]');
  const chinese = Object.fromEntries(Array.from(fields, field =>
    [field.dataset.copy, field.textContent]));

  const translations = {
    zh: {
      ...chinese, lang: 'zh-CN', title: document.title,
      description: description.content, menu: menu.getAttribute('aria-label'),
      page: 'kousei.html', guideFile: 'Readme.txt', navigation: '栏目'
    },
    en: {
      lang: 'en', title: 'Heigao’s Voicebanks',
      description: 'Explore Heigao’s voicebanks, listen to demos, and find character profiles, downloads, and terms of use.',
      menu: 'Choose a language', catalog: 'Voicebank catalog',
      navigation: 'Sections', shelf: 'Voicebanks', assets: 'Resources', journal: 'Voicebank journal',
      noAssets: 'No resources are available for download yet.', noEntries: 'No entries yet.',
      name: 'Shang Wei Yin Kousei', format: 'Japanese UTAU voicebank',
      voices: 'Soft, Original, and Falsetto', enter: 'Explore voicebank',
      starName: 'Shang Wei Yin Kousei (恒星)', ai: 'AI voicebank', unreleased: 'Not yet released',
      guide: 'Voicebank Guide V1.1', download: 'Download', readGuide: 'Read the guide',
      guideNote: 'This guide covers recording pitches for all three voice styles, the character profile, and the terms of use.',
      namesake: 'Named after the star HR 4796A.',
      starDescription: 'Kousei (恒星) is an unreleased AI voicebank.',
      page: 'index-en.html', guideFile: 'Readme_EN.txt'
    },
    ja: {
      lang: 'ja', title: '黒篙の音源一覧 | Heigao’s Voicebanks',
      description: '黒篙が配布している音源の一覧です。各音源のページで試聴、キャラクター紹介、ダウンロード、利用規約をご覧いただけます。',
      menu: '言語を選択', catalog: '黒篙の音源一覧',
      navigation: 'サイトメニュー', shelf: '音源一覧', assets: '配布素材', journal: '制作日誌',
      noAssets: '現在配布中の素材はありません。', noEntries: 'まだ記事はありません。',
      name: '熵尾音 こうせい', format: '日本語UTAU音源',
      voices: 'ソフト・地声・裏声', enter: '音源ページへ',
      starName: '熵尾音 恒星', ai: 'AI歌声音源', unreleased: '未公開',
      guide: 'V1.1 利用ガイド', download: 'ダウンロード', readGuide: 'ガイドを読む',
      guideNote: '3種類の声色の収録音高、キャラクター設定、利用規約を掲載しています。',
      namesake: '名前の由来は恒星 HR 4796A です。',
      starDescription: '熵尾音 恒星（こうせい）は、現在未公開のAI歌声音源です。',
      page: 'index-jp.html', guideFile: 'Readme_JP.txt'
    }
  };

  function updateLanguage() {
    const code = location.hash.slice(1);
    const lang = Object.hasOwn(translations, code) ? code : 'zh';
    const copy = translations[lang];
    document.documentElement.lang = copy.lang;
    document.title = sections || lang === 'zh' ? copy.title : copy.starName + ' | Heigao’s Voicebanks';
    description.content = sections || lang === 'zh' ? copy.description : copy.starDescription;
    for (const field of fields) field.textContent = copy[field.dataset.copy];
    const suffix = lang === 'zh' ? '' : '#' + lang;
    const urls = { page: copy.page, guidePage: copy.page + '#guidelines', guideFile: copy.guideFile,
      stellar: 'hengxing.html' + suffix, home: 'index.html' + suffix };
    for (const link of localizedLinks) link.setAttribute('href', urls[link.dataset.localLink]);
    menu.setAttribute('aria-label', copy.menu);
    sections?.setAttribute('aria-label', copy.navigation);
    for (const link of menu.querySelectorAll('a')) {
      if (link.lang === copy.lang) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    }
  }

  function wirePanels(buttons) {
    for (const button of buttons) {
      button.addEventListener('click', () => {
        for (const item of buttons) {
          const active = item === button;
          document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
          item.setAttribute('aria-pressed', String(active));
        }
      });
    }
  }

  updateLanguage();
  wirePanels(sectionButtons);
  for (const picker of document.querySelectorAll('.bank-picker')) {
    wirePanels(picker.querySelectorAll('button'));
  }
  if (sections) sections.hidden = false;
  menu.hidden = false;
  window.addEventListener('hashchange', updateLanguage);

  if ('IntersectionObserver' in window && matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('arriving');
        observer.unobserve(entry.target);
      }
    });
    for (const release of document.querySelectorAll('#shelf .release + .release')) {
      if (release.getBoundingClientRect().top >= innerHeight) observer.observe(release);
    }
  }
})();
