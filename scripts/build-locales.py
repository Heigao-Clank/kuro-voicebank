#!/usr/bin/env python3
"""Build the three static pages from the Chinese page layout and the bundled voicebank guides."""
import argparse
import hashlib
import re
from pathlib import Path
from site_content import render_pages
from locale_messages import build_messages

ROOT = Path(__file__).resolve().parent.parent


def apply(src: str, L: dict) -> str:
    out = src
    swaps = [
        ('<html lang="zh-CN"><head>', f'<html lang="{L["lang"]}"><head>'),
        ('<title>熵尾音 咬青 | UTAU Voicebank</title>', f'<title>{L["title"]}</title>'),
        (
            '<meta property="og:title" content="熵尾音 咬青 | UTAU Voicebank">',
            f'<meta property="og:title" content="{L["title"]}">',
        ),
    ]
    for old, new in swaps:
        if old not in out:
            raise RuntimeError(f'missing anchor: {old[:60]}')
        out = out.replace(old, new, 1)

    # Background deco lines
    deco_old = [
        '<div class="bg-deco-text">熵尾咬青 熵尾咬青 熵尾咬青 </div>',
        '<div class="bg-deco-text">UTAU • JA VCV&amp;CVVC UTAU • JA VCV&amp;CVVC </div>',
        '<div class="bg-deco-text">感谢使用 感谢使用 感谢使用 </div>',
    ]
    out = out.replace('熵尾音 咬青 熵尾音 咬青 熵尾音 咬青 ', '熵尾咬青 熵尾咬青 熵尾咬青 ')
    for old, new in zip(deco_old, L['bg']):
        out = out.replace(old, f'<div class="bg-deco-text">{new}</div>')

    # Topnav / sidebar brand
    out = out.replace(
        '<span class="topnav-brand-text">熵尾音 咬青<small>UTAU Voicebank</small></span>',
        f'<span class="topnav-brand-text">{L["brand"]}<small>UTAU Voicebank</small></span>',
        1,
    )
    out = out.replace(
        '<span class="sidebar-brand-text">熵尾音 咬青<br><small style="font-weight:400;color:var(--text-muted);font-size:0.7rem;">UTAU Voicebank</small></span>',
        f'<span class="sidebar-brand-text">{L["brand"]}<br><small style="font-weight:400;color:var(--text-muted);font-size:0.7rem;">UTAU Voicebank</small></span>',
        1,
    )

    # Topnav nav (replace the anchor block)
    topnav_old = '''    <nav class="topnav-nav" aria-label="主要导航">
      <a href="#demo" class="topnav-link">试听</a>
      <a href="#profile" class="topnav-link">档案</a>
      <a href="#download" class="topnav-link">下载</a>
      <a href="#guidelines" class="topnav-link">协议</a>
      <a href="#faq" class="topnav-link">FAQ</a>
      <a href="#contact" class="topnav-link">联系</a>
    </nav>'''
    topnav_new = f'''    <nav class="topnav-nav" aria-label="{L["navigation"]}">
      <a href="#demo" class="topnav-link">{L["nav"][0]}</a>
      <a href="#profile" class="topnav-link">{L["nav"][1]}</a>
      <a href="#download" class="topnav-link">{L["nav"][2]}</a>
      <a href="#guidelines" class="topnav-link">{L["nav"][3]}</a>
      <a href="#faq" class="topnav-link">{L["nav"][4]}</a>
      <a href="#contact" class="topnav-link">{L["nav"][5]}</a>
    </nav>'''
    out = out.replace(topnav_old, topnav_new, 1)

    # Lang switcher
    lang_old = '''    <div class="lang-switcher topnav-lang">
      <a href="index.html" class="active">中文</a>
      <a href="index-en.html">EN</a>
      <a href="index-jp.html">日本語</a>
    </div>'''
    lang_new = f'''    <div class="lang-switcher topnav-lang">
      <a href="index.html"{' class="active"' if L['lang'] == 'zh' else ''}>中文</a>
      <a href="index-en.html"{' class="active"' if L['lang'] == 'en' else ''}>EN</a>
      <a href="index-jp.html"{' class="active"' if L['lang'] == 'ja' else ''}>日本語</a>
    </div>'''
    out = out.replace(lang_old, lang_new, 1)

    # Sidebar navigation labels
    side_text = {
        '首页': 'home',
        '试听演示': 'demo',
        '角色档案': 'profile',
        '下载音源': 'download',
        '使用协议': 'guidelines',
        '常见问题': 'faq',
        '联系方式': 'contact',
    }
    for zh, key in side_text.items():
        out = out.replace(f'<span class="sidebar-nav-text">{zh}</span>', f'<span class="sidebar-nav-text">{L["side_nav"][key]}</span>', 1)
    out = out.replace('<span>作者个人网站</span>', f'<span>{L["side_nav"]["site"]}</span>', 1)

    # Section titles (use single-line p tags inside section-title block)
    sec_titles = [
        ('<h2>试听演示</h2>\n          <p>Voice Demo</p>', f'<h2>{L["demo_title"]}</h2>\n          <p>{L["demo_sub"]}</p>'),
        ('<h2>角色档案</h2>\n          <p>Character Profile</p>', f'<h2>{L["profile_title"]}</h2>\n          <p>{L["profile_sub"]}</p>'),
        ('<h2>下载音源</h2>\n          <p>Download</p>', f'<h2>{L["download_title"]}</h2>\n          <p>{L["download_sub"]}</p>'),
        ('<h2>使用协议</h2>\n          <p>Usage Guidelines</p>', f'<h2>{L["guidelines_title"]}</h2>\n          <p>{L["guidelines_sub"]}</p>'),
        ('<h2>常见问题</h2>\n          <p>FAQ</p>', f'<h2>{L["faq_title"]}</h2>\n          <p>{L["faq_sub"]}</p>'),
        ('<h2>联系方式</h2>\n          <p>Contact</p>', f'<h2>{L["contact_section_title"]}</h2>\n          <p>{L["contact_section_sub"]}</p>'),
    ]
    for old, new in sec_titles:
        out = out.replace(old, new, 1)

    # Download accordion 1 (GitHub)
    cp_old = '''<button type="button" class="install-copy" aria-label="复制命令" title="复制命令" hidden>'''
    cp_new = f'''<button type="button" class="install-copy" aria-label="{L["install_label"]}" title="{L["install_title"]}" hidden>'''
    out = out.replace(cp_old, cp_new, 1)
    # Cloud storage
    cs_old = '''                <span class="accordion-name">网盘下载</span>'''
    cs_new = f'''                <span class="accordion-name">{L["cloud_section"]}</span>'''
    out = out.replace(cs_old, cs_new, 1)
    cs_old2 = '''                <p class="accordion-desc">备用下载方式</p>'''
    cs_new2 = f'''                <p class="accordion-desc">{L["cloud_description"]}</p>'''
    out = out.replace(cs_old2, cs_new2, 1)
    out = out.replace('class="accordion-link">123云盘</a>', f'class="accordion-link">{L["cloud_name"]}</a>', 1)
    out = out.replace('密码：<code', f'{L["pass_label"]}<code', 1)
    out = out.replace('this.title=\'已复制\'', f'this.title=\'{L["install_copied"]}\'', 1)
    out = out.replace('title="点击复制"', f'title="{L["copy_tooltip"]}"', 1)

    # Contact section: 4 cards
    items = L['contact_field']
    contact_block_old = '''        <div class="contact-grid">
          <a href="mailto:heigao75@qq.com" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"></rect><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path></svg></div>
            <div>
              <div class="profile-label">Email</div>
              <div class="profile-value">heigao75@qq.com</div>
            </div>
          </a>
          <a href="https://twitter.com/heigao_tickle" target="_blank" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path></svg></div>
            <div>
              <div class="profile-label">Twitter/X</div>
              <div class="profile-value">@heigao_tickle</div>
            </div>
          </a>
          <a href="https://space.bilibili.com/695724697" target="_blank" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="15" x="2" y="7" rx="2" ry="2"></rect><polyline points="17 2 12 7 7 2"></polyline></svg></div>
            <div>
              <div class="profile-label">Bilibili</div>
              <div class="profile-value">黑篙</div>
            </div>
          </a>
          <a href="https://heigao.me/" target="_blank" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></circle><path d="M2 12h20"></path></svg></div>
            <div>
              <div class="profile-label">个人网站</div>
              <div class="profile-value">heigao.me</div>
            </div>
          </a>
        </div>'''
    contact_block_new = f'''        <div class="contact-grid">
          <a href="{items[0][2]}" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"></rect><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path></svg></div>
            <div>
              <div class="profile-label">{items[0][0]}</div>
              <div class="profile-value">{items[0][1]}</div>
            </div>
          </a>
          <a href="https://twitter.com/heigao_tickle" target="_blank" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path></svg></div>
            <div>
              <div class="profile-label">{items[1][0]}</div>
              <div class="profile-value">{items[1][1]}</div>
            </div>
          </a>
          <a href="https://space.bilibili.com/695724697" target="_blank" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="15" x="2" y="7" rx="2" ry="2"></rect><polyline points="17 2 12 7 7 2"></polyline></svg></div>
            <div>
              <div class="profile-label">{items[2][0]}</div>
              <div class="profile-value">{items[2][1]}</div>
            </div>
          </a>
          <a href="https://heigao.me/" target="_blank" class="contact-item">
            <div class="contact-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></circle><path d="M2 12h20"></path></svg></div>
            <div>
              <div class="profile-label">{items[3][0]}</div>
              <div class="profile-value">{items[3][1]}</div>
            </div>
          </a>
        </div>'''
    out = out.replace(contact_block_old, contact_block_new, 1)

    # Footer
    out = out.replace(
        '<p class="footer-text">熵尾音 咬青 UTAU Voicebank</p>',
        f'<p class="footer-text">{L["footer_title"]}</p>',
        1,
    )
    out = out.replace(
        '<p class="footer-copyright">© 2026 黑篙 All Rights Reserved.</p>',
        f'<p class="footer-copyright">{L["footer_cr"]}</p>',
        1,
    )

    return out


def locale_en():
    return {
        'lang': 'en',
        'navigation': 'Main navigation',
        'self': 'index-en.html',
        'title': 'Shang Wei Yin Kousei | UTAU Voicebank',
        'brand': 'Shang Wei Yin Kousei',
        'bg': ['SHANG WEI YIN KOUSEI SHANG WEI YIN KOUSEI SHANG WEI YIN KOUSEI ',
               'UTAU • JA VCV&amp;CVVC UTAU • JA VCV&amp;CVVC ',
               'THANK YOU FOR USING THANK YOU FOR USING '],
        'nav': ['Voice Demo', 'Profile', 'Download', 'Guidelines', 'FAQ', 'Contact'],
        'side_nav': {'home': 'Home', 'demo': 'Voice Demo', 'profile': 'Profile',
                     'download': 'Download', 'guidelines': 'Guidelines', 'faq': 'FAQ',
                     'contact': 'Contact', 'site': 'Personal Website'},
        'demo_title': 'Voice Demo',
        'demo_sub': 'Listen to the voicebank',
        'profile_title': 'Character Profile',
        'profile_sub': 'Details and personality',
        'download_title': 'Download',
        'download_sub': 'Get the latest version',
        'cloud_section': 'Cloud Storage', 'cloud_description': 'V1 download mirrors', 'cloud_name': '123 Cloud',
        'install_label': 'Copy command',
        'install_title': 'Copy command',
        'install_copied': 'Copied',
        'copy_tooltip': 'Click to copy',
        'pass_label': 'Password: ',
        'guidelines_title': 'Usage Guidelines',
        'guidelines_sub': 'Usage Guidelines',
        'faq_title': 'FAQ',
        'faq_sub': 'FAQ',
        'contact_section_title': 'Contact',
        'contact_section_sub': 'Contact',
        'contact_field': [
            ('Email', 'heigao75@qq.com', 'mailto:heigao75@qq.com'),
            ('Twitter/X', '@heigao_tickle', 'https://twitter.com/heigao_tickle'),
            ('Bilibili', 'Heigao', 'https://space.bilibili.com/695724697'),
            ('Personal Site', 'heigao.me', 'https://heigao.me/'),
        ],
        'footer_title': 'Shang Wei Yin Kousei UTAU Voicebank',
        'footer_cr': '© 2026 Heigao All Rights Reserved.',
    }


def locale_jp():
    return {
        'lang': 'ja',
        'navigation': 'メインナビゲーション',
        'self': 'index-jp.html',
        'title': '熵尾音 こうせい | UTAU Voicebank',
        'brand': '熵尾音 こうせい',
        'bg': ['熵尾音 こうせい 熵尾音 こうせい 熵尾音 こうせい ',
               'UTAU • JA VCV&amp;CVVC UTAU • JA VCV&amp;CVVC ',
               'ご利用ありがとうございます '],
        'nav': ['試聴', 'プロフィール', 'ダウンロード', '規約', 'FAQ', '連絡先'],
        'side_nav': {'home': 'ホーム', 'demo': '試聴', 'profile': 'プロフィール',
                     'download': 'ダウンロード', 'guidelines': '規約',
                     'faq': 'よくある質問', 'contact': '連絡先', 'site': '個人サイト'},
        'demo_title': '試聴デモ',
        'demo_sub': 'ボイスバンクを聴く',
        'profile_title': 'プロフィール',
        'profile_sub': 'キャラクター紹介',
        'download_title': 'ダウンロード',
        'download_sub': '最新版を取得',
        'cloud_section': 'クラウド', 'cloud_description': 'V1のミラー配布先', 'cloud_name': '123クラウド',
        'install_label': 'コマンドをコピー',
        'install_title': 'コマンドをコピー',
        'install_copied': 'コピーしました',
        'copy_tooltip': 'クリックしてコピー',
        'pass_label': 'パスワード：',
        'guidelines_title': '使用規約',
        'guidelines_sub': '利用規約',
        'faq_title': 'よくある質問',
        'faq_sub': 'FAQ',
        'contact_section_title': '連絡先',
        'contact_section_sub': 'お問い合わせ',
        'contact_field': [
            ('Email', 'heigao75@qq.com', 'mailto:heigao75@qq.com'),
            ('Twitter/X', '@heigao_tickle', 'https://twitter.com/heigao_tickle'),
            ('Bilibili', '黒篙', 'https://space.bilibili.com/695724697'),
            ('個人サイト', 'heigao.me', 'https://heigao.me/'),
        ],
        'footer_title': '熵尾音 こうせい UTAU Voicebank',
        'footer_cr': '© 2026 黒篙 All Rights Reserved.',
    }


def version_asset(html, directory, asset):
    digest = hashlib.sha256((directory / asset).read_bytes()).hexdigest()[:12]
    pattern = '"' + re.escape(asset) + r'(?:\?v=[0-9a-f]+)?"'
    updated, count = re.subn(pattern, f'"{asset}?v={digest}"', html)
    if count != 1:
        raise ValueError(f'Expected one reference to {asset}, found {count}')
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report stale pages without writing files.')
    args = parser.parse_args()
    src = (ROOT / 'index.html').read_text()
    src = re.sub(r' data-msg(?:-version)?="[^"]*"', "", src)
    for asset in ('style.css', 'assets/mobile-cover.css', 'assets/main.js'):
        src = version_asset(src, ROOT, asset)
    shells = {'zh': src, 'en': apply(src, locale_en()), 'jp': apply(src, locale_jp())}
    pages = render_pages(ROOT, shells)
    build_messages(pages)
    archive = ROOT / 'assets/terms-v1.html'
    pages['assets/terms-v1.html'] = version_asset(archive.read_text(), archive.parent, '../style.css')
    stale = []
    for name, text in pages.items():
        page = ROOT / name
        content = text.encode('utf-8')
        if not page.exists() or page.read_bytes() != content:
            if args.check:
                stale.append(name)
            else:
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_bytes(content)
    if stale:
        raise SystemExit('Rebuild with python3 scripts/build-locales.py: ' + ', '.join(stale))


if __name__ == '__main__':
    main()
