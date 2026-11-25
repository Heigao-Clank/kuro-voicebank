// Run against the generated static files, or pass the URL of a local preview server.
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const root = process.argv[2] || pathToFileURL(path.resolve(__dirname, '..') + path.sep).href;
const locales = [['kousei.html', 'zh'], ['index-en.html', 'en'], ['index-jp.html', 'jp']];

async function checkCatalog(browser) {
  const page = await browser.newPage({reducedMotion: 'reduce'});
  try {
    for (const width of [320, 390, 768, 1440]) {
      await page.setViewportSize({width, height: 844});
      await page.goto(new URL('index.html', root).href);
      const release = page.getByRole('link', {name: '熵尾音 咬青 进入声库'});
      await release.locator('img').evaluate(img => img.decode());
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await release.click();
      assert.equal(new URL(page.url()).pathname.split('/').pop(), 'kousei.html');
      await page.locator('.footer-catalog').click();
      assert.ok(await release.isVisible());
      const menu = page.locator('.catalog-languages');
      for (const [code, target] of [['en', 'index-en.html'], ['ja', 'index-jp.html'], ['zh-CN', 'kousei.html']]) {
        const requests = [];
        const onRequest = request => requests.push(request.url());
        page.on('request', onRequest);
        await menu.locator('a[lang="' + code + '"]').click();
        await page.waitForFunction(lang => document.documentElement.lang === lang, code);
        page.off('request', onRequest);
        assert.deepEqual(requests, []);
        assert.equal(await menu.locator('[aria-current="true"]').getAttribute('lang'), code);
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
        assert.equal(await page.locator('[data-local-link="page"]').getAttribute('href'), target);
      }
    }
    for (const [lang, guideFile] of [['zh-CN', 'Readme.txt'], ['en', 'Readme_EN.txt'], ['ja', 'Readme_JP.txt']]) {
      await page.locator('.catalog-languages a[lang="' + lang + '"]').click();
      await page.waitForFunction(lang => document.documentElement.lang === lang, lang);
      await page.locator('[data-section="assets"]').click();
      const assets = page.locator('#assets');
      await assets.locator('[aria-controls="stellar-assets"]').click();
      assert.ok(await page.locator('#stellar-assets').isVisible());
      assert.ok(await page.locator('#kousei-assets').isHidden());
      await assets.locator('[aria-controls="kousei-assets"]').click();
      assert.ok(await assets.locator('[download]').isVisible());
      assert.equal(await page.locator('[download]').getAttribute('href'), guideFile);
      await page.locator('[data-section="journal"]').click();
      await page.locator('[aria-controls="stellar-journal"]').click();
      assert.ok(await page.locator('#stellar-journal').isVisible());
      assert.ok(await page.locator('#kousei-journal').isHidden());
      await page.locator('[data-section="shelf"]').click();
      await page.locator('[data-local-link="stellar"]').click();
      assert.ok(await page.locator('.release-status').isVisible());
      assert.equal(await page.locator('html').getAttribute('lang'), lang);
      await page.locator('.back-link').click();
      assert.equal(await page.locator('html').getAttribute('lang'), lang);
    }
    await page.locator('.catalog-languages [lang="en"]').click();
    await page.locator('.release[href="index-en.html"]').click();
    await page.locator('.topnav-lang a[lang="ja"]').click();
    await page.locator('.footer-catalog[href="index.html#ja"]').click();
    await page.waitForFunction(() => document.documentElement.lang === 'ja');
    await page.reload();
    assert.equal(await page.locator('#kousei-name').innerText(), '熵尾音 こうせい');
    for (const hash of ['#guidelines', '#demo', '#faq-answer-3']) {
      await page.goto(new URL('index.html' + hash, root).href);
      await page.waitForURL('**/kousei.html' + hash);
      assert.equal(await page.locator(hash).count(), 1);
    }
  } finally {
    await page.close();
  }
}

async function checkLocale(browser, file, lang) {
  const page = await browser.newPage({ viewport: {width: 390, height: 844}, reducedMotion: 'reduce' });
  try {
    const requests = [];
    page.on('request', request => requests.push(request.url()));
    await page.goto(new URL(file + '#contact', root).href);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForFunction(() => {
      const link = document.querySelector('.topnav-link[aria-current="location"]');
      const nav = document.querySelector('.topnav-nav').getBoundingClientRect();
      const box = link?.getBoundingClientRect();
      return link?.hash === '#contact' && box.left >= nav.left - 1 && box.right <= nav.right + 1;
    });
    assert.equal(await page.locator('.protocol-content:visible').getAttribute('id'), 'protocol-' + lang);
    for (const code of ['en', 'jp', 'zh']) {
      await page.emulateMedia({media:'screen'});
      await page.locator('.protocol-tab[data-lang="' + code + '"]').click();
      await page.emulateMedia({media:'print'});
      const panel = page.locator('.protocol-content:visible');
      assert.equal(await panel.count(), 1);
      assert.equal(await panel.getAttribute('id'), 'protocol-' + code);
      assert.ok(await panel.evaluate(el => el.clientHeight >= el.scrollHeight - 1), 'Printed terms are clipped');
    }
    assert.ok(!requests.some(url => url.endsWith('/protocol-content.js') || url.endsWith('/icons.js')));
  } finally {
    await page.close();
  }
}

async function checkNativeControls(browser, file) {
  const page = await browser.newPage({javaScriptEnabled: false, reducedMotion: 'reduce'});
  try {
    await page.goto(new URL(file + '#download', root).href);
    const github = page.locator('#download details').first();
    await github.locator('summary').focus();
    await page.keyboard.press('Enter');
    assert.ok(await github.evaluate(el => el.open));
    assert.ok(await github.locator('a[href$="/tag/V1"]').isVisible());
    const mirrors = page.locator('#download details').last();
    await mirrors.locator('summary').focus();
    await page.keyboard.press('Space');
    assert.equal(await mirrors.locator('a:visible').count(), 2);
    assert.ok(await github.locator('.install-copy').isHidden());
    const faq = page.locator('.faq-item').first();
    await faq.locator('summary').focus();
    await page.keyboard.press('Enter');
    assert.ok(await faq.locator('.faq-answer').isVisible());
  } finally {
    await page.close();
  }
}

async function checkAudio(browser, file) {
  const page = await browser.newPage({reducedMotion:'reduce'});
  try {
    let blockMp3 = true;
    await page.route('**/demo-01.opus', route => route.abort());
    await page.route('**/demo-01.mp3', route => blockMp3 ? route.abort() : route.continue());
    await page.goto(new URL(file + '#demo', root).href);
    const card = page.locator('.demo-card').first();
    const button = card.locator('.demo-play-btn');
    const slider = card.locator('.demo-progress');
    await button.click();
    await page.waitForFunction(() => document.querySelector('.demo-status').textContent.length > 0);
    assert.ok(await card.locator('.icon-pause').isHidden());

    blockMp3 = false;
    await button.click();
    await page.waitForFunction(() => document.querySelector('audio').currentTime > 0);
    assert.equal(await card.locator('.demo-status').textContent(), '');
    assert.ok(await card.locator('audio').evaluate(el => el.currentSrc.endsWith('.mp3')));
    await slider.focus();
    await page.keyboard.press('End');
    await page.waitForFunction(() => document.querySelector('audio').ended);
    const [current, duration] = (await card.locator('.demo-time').innerText()).split(' / ');
    assert.equal(current, duration);
    assert.equal(await slider.getAttribute('aria-valuenow'), await slider.getAttribute('aria-valuemax'));
    await button.click();
    await page.waitForFunction(() => {
      const a = document.querySelector('audio');
      return !a.paused && a.currentTime > 0 && a.currentTime < 3;
    });
  } finally {
    await page.close();
  }
}

async function checkPendingLanguage(browser) {
  const page = await browser.newPage({viewport: {width: 390, height: 844}, reducedMotion: 'reduce'});
  try {
    await page.goto(new URL('kousei.html#faq', root).href);
    const english = page.locator('.topnav-lang a[lang="en"]');
    const japanese = page.locator('.topnav-lang a[lang="ja"]');
    await page.route(/\/locales\/en\.js\?/, route => route.abort());
    await english.click();
    await page.locator('.topnav-lang [role="status"]').waitFor();
    assert.equal(await page.locator('html').getAttribute('lang'), 'zh-CN');
    await page.unroute(/\/locales\/en\.js\?/);

    let release;
    const pending = new Promise(resolve => { release = resolve; });
    await page.route(/\/locales\/en\.js\?/, async route => { await pending; await route.continue(); });
    const requested = page.waitForRequest(req => req.url().includes('/locales/en.js'));
    await english.click();
    await requested;
    const question = page.locator('.faq-item').nth(3);
    await question.evaluate(el => {
      el.open = true;
      window.scrollBy({top: el.getBoundingClientRect().top - document.querySelector('.topnav').offsetHeight, behavior: 'instant'});
    });
    const top = await question.evaluate(el => el.getBoundingClientRect().top);
    await japanese.click();
    await page.waitForFunction(() => document.documentElement.lang === 'ja');
    assert.ok(Math.abs(await question.evaluate(el => el.getBoundingClientRect().top) - top) < 4);
    const response = page.waitForEvent('requestfinished', r => r.url().includes('/locales/en.js'));
    release();
    await response;
    assert.equal(await page.locator('html').getAttribute('lang'), 'ja');
    await english.click();
    await page.waitForFunction(() => document.documentElement.lang === 'en');
    assert.ok(await question.evaluate(el => el.open));
    assert.equal(await page.locator('.topnav-lang [role="status"]').count(), 0);
  } finally {
    await page.close();
  }
}

async function checkLanguageSwitch(browser) {
  for (const width of [390, 1440]) {
    const page = await browser.newPage({viewport: {width, height: 844}, reducedMotion: 'reduce'});
    const errors = [];
    const requests = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', request => requests.push(new URL(request.url()).pathname));
    const snapshot = () => page.evaluate(() => ({
      title: document.title,
      fields: Array.from(document.querySelectorAll('[data-msg]'), element =>
        element.dataset.msg.split(' ').map(key => {
          if (key === 'lines') return element.innerHTML;
          if (!/^\d+$/.test(key)) return element.getAttribute(key);
          return Array.from(element.childNodes).filter(n => n.nodeType === 3 && n.data.trim())[Number(key)].data;
        })),
      protocol: document.querySelector('.protocol-content:not([hidden])').lang,
      slider: document.querySelector('.demo-progress').getAttribute('aria-label')
    }));
    const initial = {};
    try {
      for (const [file] of locales) {
        await page.goto(new URL(file, root).href);
        initial[await page.locator('html').getAttribute('lang')] = await snapshot();
      }
      const langLink = lang => page.locator('.topnav-lang a[lang="' + lang + '"]');
      for (const [file] of locales) {
        await page.goto(new URL(file + '#demo', root).href);
        const start = await page.locator('html').getAttribute('lang');
        const url = page.url();
        requests.length = 0;
        await page.locator('.demo-play-btn').first().click();
        await page.waitForFunction(() => document.querySelector('audio').currentTime > 0);
        await page.evaluate(() => {
          window.originalPlayer = document.querySelector('audio');
          document.querySelector('.faq-item').open = true;
          document.querySelector('.accordion').open = true;
        });
        const sequence = Object.keys(initial).filter(lang => lang !== start);
        for (const lang of [...sequence, start, ...sequence]) {
          await langLink(lang).click();
          await page.waitForFunction(lang => document.documentElement.lang === lang, lang);
          assert.deepEqual(await snapshot(), initial[lang]);
          assert.equal(page.url(), url);
          assert.ok(await page.evaluate(() =>
            document.querySelector('audio') === window.originalPlayer && !window.originalPlayer.paused &&
            document.querySelector('.faq-item').open && document.querySelector('.accordion').open));
        }
        assert.equal(requests.filter(url => url.includes('/locales/')).length, 2);
        assert.ok(!requests.some(url => url.endsWith('.html')));
      }
      assert.deepEqual(errors, []);
    } finally {
      await page.close();
    }
  }
}

(async () => {
  const browser = await chromium.launch({executablePath:process.env.CHROME_PATH});
  try {
    await checkCatalog(browser);
    if (!root.startsWith('file:')) await checkPendingLanguage(browser);
    await checkLanguageSwitch(browser);
    for (const [file, lang] of locales) {
      await checkLocale(browser, file, lang);
      await checkNativeControls(browser, file);
      await checkAudio(browser, file);
      console.log(file + ' passed');
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
