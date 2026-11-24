// Run against the generated static files, or pass the URL of a local preview server.
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const root = process.argv[2] || pathToFileURL(path.resolve(__dirname, '..') + path.sep).href;
const locales = [['index.html', 'zh'], ['index-en.html', 'en'], ['index-jp.html', 'jp']];

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

(async () => {
  const browser = await chromium.launch({executablePath:process.env.CHROME_PATH});
  try {
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
