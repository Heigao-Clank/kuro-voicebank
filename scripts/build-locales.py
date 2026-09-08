#!/usr/bin/env python3
"""Build index-en.html and index-jp.html from index.html in the restore folder."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text()


def apply(src: str, L: dict) -> str:
    out = src
    swaps = [
        ('<html lang="zh-CN"><head>', f'<html lang="{L["lang"]}"><head>'),
        ('<title>熵尾音 咬青 | UTAU Voicebank</title>', f'<title>{L["title"]}</title>'),
        (
            '<meta name="description" content="「熵尾音 咬青」UTAU 日语音源，JA VCV&amp;CVVC 双尾狼兽人声库。免费下载，可用于翻唱、Vocaloid风二创。面纹特征，自信懵懂声线。制作：黑篙。">',
            f'<meta name="description" content="{L["description"]}">',
        ),
        (
            '<meta property="og:title" content="熵尾音 咬青 | UTAU Voicebank">',
            f'<meta property="og:title" content="{L["title"]}">',
        ),
        (
            '<meta property="og:description" content="UTAU 音源「熵尾音 咬青」- JA VCV&amp;CVVC 日语音阶声库，推荐引擎 HiFi类引擎，支持翻唱与二创下载使用。">',
            f'<meta property="og:description" content="{L["og_desc"]}">',
        ),
    ]
    for old, new in swaps:
        if old not in out:
            raise RuntimeError(f'missing anchor: {old[:60]}')
        out = out.replace(old, new, 1)

    if L['lang'] == 'ja':
        # make the x-default the Japanese variant since we're on index-jp.html
        out = out.replace(
            '<link rel="alternate" hreflang="x-default" href="https://kuro-voicebank.pages.dev/">',
            '<link rel="alternate" hreflang="x-default" href="https://kuro-voicebank.pages.dev/index-jp.html">',
            1,
        )

    # Background deco lines
    deco_old = [
        '<div class="bg-deco-text">熵尾咬青 熵尾咬青 熵尾咬青 </div>',
        '<div class="bg-deco-text">UTAU • JA VCV&amp;CVVC UTAU • JA VCV&amp;CVVC </div>',
        '<div class="bg-deco-text">感谢使用 感谢使用 感谢使用 </div>',
    ]
    for old, new in zip(deco_old, L['bg']):
        out = out.replace(old, f'<div class="bg-deco-text">{new}</div>', 1)

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
      <a href="index.html#demo" class="topnav-link">试听</a>
      <a href="index.html#profile" class="topnav-link">档案</a>
      <a href="index.html#voicebank" class="topnav-link">音源</a>
      <a href="index.html#download" class="topnav-link">下载</a>
      <a href="index.html#guidelines" class="topnav-link">协议</a>
      <a href="index.html#faq" class="topnav-link">FAQ</a>
      <a href="index.html#contact" class="topnav-link">联系</a>
    </nav>'''
    topnav_new = f'''    <nav class="topnav-nav" aria-label="{L["side_nav"]["home"]}">
      <a href="{L["self"]}#demo" class="topnav-link">{L["nav"][0]}</a>
      <a href="{L["self"]}#profile" class="topnav-link">{L["nav"][1]}</a>
      <a href="{L["self"]}#voicebank" class="topnav-link">{L["nav"][2]}</a>
      <a href="{L["self"]}#download" class="topnav-link">{L["nav"][3]}</a>
      <a href="{L["self"]}#guidelines" class="topnav-link">{L["nav"][4]}</a>
      <a href="{L["self"]}#faq" class="topnav-link">{L["nav"][5]}</a>
      <a href="{L["self"]}#contact" class="topnav-link">{L["nav"][6]}</a>
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
      <a href="index-jp.html"{' class="active"' if L['lang'] == 'jp' else ''}>日本語</a>
    </div>'''
    out = out.replace(lang_old, lang_new, 1)

    # Sidebar anchors + nav text
    for href in ['hero', 'demo', 'profile', 'voicebank', 'download', 'guidelines', 'faq', 'contact']:
        out = out.replace(f'<a href="index.html#{href}"', f'<a href="{L["self"]}#{href}"')

    side_text = {
        '首页': 'home',
        '试听演示': 'demo',
        '角色档案': 'profile',
        '音源信息': 'voicebank',
        '下载音源': 'download',
        '使用协议': 'guidelines',
        '常见问题': 'faq',
        '联系方式': 'contact',
    }
    for zh, key in side_text.items():
        out = out.replace(f'<span class="sidebar-nav-text">{zh}</span>', f'<span class="sidebar-nav-text">{L["side_nav"][key]}</span>', 1)
    out = out.replace('<span>作者个人网站</span>', f'<span>{L["side_nav"]["site"]}</span>', 1)

    # Hero block
    hero_old = '''    <!-- Hero Section - 1024Store Style -->
    <section class="hero" id="hero">
      <div class="container">
        <div class="hero-stage">
          <div class="hero-main">
            <div class="hero-visual">
              <picture>
                <source media="(max-width: 600px)" srcset="assets/images/character-320w.webp">
                <img src="assets/images/character.webp" alt="熵尾音 咬青" class="hero-character" onerror="this.style.display='none'">
              </picture>
              <p class="hero-visual-text">插图 · 黑篙</p>
            </div>
            <div class="hero-text">
              <p class="hero-eyebrow">UTAU VOICEBANK</p>
              <h1 class="hero-title">熵尾音 咬青</h1>
              <p class="hero-subtitle">UTAU 日语音库 · <span class="vb-type">JA VCV&amp;CVVC</span></p>
              <p class="hero-description">
                双尾狼兽人 · 面纹<br>
                <span class="text-muted">未知天外来物的独立子体</span>
              </p>
              <div class="hero-download">
                <a href="index.html#download" class="btn btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg>
                  下载音源</a>
                <a href="index.html#guidelines" class="btn btn-secondary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg> 使用协议</a>
              </div>
            </div>
          </div>
          <dl class="hero-tally" aria-label="音源规格">'''
    hero_new = f'''    <!-- Hero Section - 1024Store Style -->
    <section class="hero" id="hero">
      <div class="container">
        <div class="hero-stage">
          <div class="hero-main">
            <div class="hero-visual">
              <picture>
                <source media="(max-width: 600px)" srcset="assets/images/character-320w.webp">
                <img src="assets/images/character.webp" alt="{L["hero_alt"]}" class="hero-character" onerror="this.style.display='none'">
              </picture>
              <p class="hero-visual-text">{L["hero_caption"]}</p>
            </div>
            <div class="hero-text">
              <p class="hero-eyebrow">UTAU VOICEBANK</p>
              <h1 class="hero-title">{L["hero_title"]}</h1>
              <p class="hero-subtitle">{L["hero_subtitle"]}</p>
              <p class="hero-description">{L["hero_desc"]}</p>
              <div class="hero-download">
                <a href="{L["self"]}#download" class="btn btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg>
                  {L["hero_btn1"]}</a>
                <a href="{L["self"]}#guidelines" class="btn btn-secondary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg> {L["hero_btn2"]}</a>
              </div>
            </div>
          </div>
          <dl class="hero-tally" aria-label="{L["hero_aria"]}">'''
    out = out.replace(hero_old, hero_new, 1)

    # Tally items
    tally_old = '''          <dl class="hero-tally" aria-label="音源规格">
            <div class="hero-tally-item">
              <dt class="hero-tally-label">语言·形式</dt>
              <dd class="hero-tally-value"><span class="vb-type">JA VCV&amp;CVVC</span></dd>
            </div>
            <div class="hero-tally-item">
              <dt class="hero-tally-label">音阶（单音阶）</dt>
              <dd class="hero-tally-value">B3</dd>
            </div>
            <div class="hero-tally-item">
              <dt class="hero-tally-label">推荐音域</dt>
              <dd class="hero-tally-value">G2~C5</dd>
            </div>
            <div class="hero-tally-item">
              <dt class="hero-tally-label">推荐引擎</dt>
              <dd class="hero-tally-value">HiFi类引擎</dd>
            </div>
          </dl>'''
    tally_new = f'''          <dl class="hero-tally" aria-label="{L["hero_aria"]}">
            <div class="hero-tally-item">
              <dt class="hero-tally-label">{L["tally_label"][0]}</dt>
              <dd class="hero-tally-value"><span class="vb-type">{L["tally_value"][0]}</span></dd>
            </div>
            <div class="hero-tally-item">
              <dt class="hero-tally-label">{L["tally_label"][1]}</dt>
              <dd class="hero-tally-value">{L["tally_value"][1]}</dd>
            </div>
            <div class="hero-tally-item">
              <dt class="hero-tally-label">{L["tally_label"][2]}</dt>
              <dd class="hero-tally-value">{L["tally_value"][2]}</dd>
            </div>
            <div class="hero-tally-item">
              <dt class="hero-tally-label">{L["tally_label"][3]}</dt>
              <dd class="hero-tally-value">{L["tally_value"][3]}</dd>
            </div>
          </dl>'''
    out = out.replace(tally_old, tally_new, 1)

    # Section titles (use single-line p tags inside section-title block)
    sec_titles = [
        ('<h2>试听演示</h2>\n          <p>Voice Demo</p>', f'<h2>{L["demo_title"]}</h2>\n          <p>{L["demo_sub"]}</p>'),
        ('<h2>角色档案</h2>\n          <p>Character Profile</p>', f'<h2>{L["profile_title"]}</h2>\n          <p>{L["profile_sub"]}</p>'),
        ('<h2>音源信息</h2>\n          <p>Voicebank Information</p>', f'<h2>{L["voicebank_title"]}</h2>\n          <p>{L["voicebank_sub"]}</p>'),
        ('<h2>下载音源</h2>\n          <p>Download</p>', f'<h2>{L["download_title"]}</h2>\n          <p>{L["download_sub"]}</p>'),
        ('<h2>使用协议</h2>\n          <p>Usage Guidelines</p>', f'<h2>{L["guidelines_title"]}</h2>\n          <p>{L["guidelines_sub"]}</p>'),
        ('<h2>常见问题</h2>\n          <p>FAQ</p>', f'<h2>{L["faq_title"]}</h2>\n          <p>{L["faq_sub"]}</p>'),
        ('<h2>联系方式</h2>\n          <p>Contact</p>', f'<h2>{L["contact_section_title"]}</h2>\n          <p>{L["contact_section_sub"]}</p>'),
    ]
    for old, new in sec_titles:
        out = out.replace(old, new, 1)

    # Demo tracks: song title and durations are kept; just replace desc and time only for changed tracks
    # JP/EN keep JP song names; durations same; no-op.

    # Profile sheet
    profile_old = '''        <div class="profile-sheet">
          <h3 class="profile-name">熵尾音 咬青</h3>
          <p class="profile-sub">双尾狼兽人 <span class="sep">·</span> 约 17 岁 <span class="sep">·</span> 168 cm</p>
          <div class="profile-divider"></div>
          <blockquote class="profile-flavor">
            <p>「未知天外来物的其中一个独立子体，容易打瞌睡，行动常由无意识驱动。面纹与双尾为天生形成，会随状态变化。」</p>
          </blockquote>
          <div class="profile-detail">
            <div class="profile-detail-row">
              <span class="profile-detail-label">声线</span>
              <span class="profile-detail-value">自信、懵懂</span>
            </div>
            <div class="profile-detail-row">
              <span class="profile-detail-label">特征</span>
              <span class="profile-detail-value">面纹、双尾（随状态变化）</span>
            </div>
            <div class="profile-detail-row">
              <span class="profile-detail-label">喜好</span>
              <span class="profile-detail-value">西瓜</span>
            </div>
          </div>
          <p class="profile-note">※ 其余设定可自由补充或进行二次创作</p>
        </div>'''
    rows = L['profile_rows']
    profile_new = f'''        <div class="profile-sheet">
          <h3 class="profile-name">{L["profile_name"]}</h3>
          <p class="profile-sub">{L["profile_meta"]}</p>
          <div class="profile-divider"></div>
          <blockquote class="profile-flavor">
            <p>{L["profile_flavor"]}</p>
          </blockquote>
          <div class="profile-detail">
            <div class="profile-detail-row">
              <span class="profile-detail-label">{rows[0][0]}</span>
              <span class="profile-detail-value">{rows[0][1]}</span>
            </div>
            <div class="profile-detail-row">
              <span class="profile-detail-label">{rows[1][0]}</span>
              <span class="profile-detail-value">{rows[1][1]}</span>
            </div>
            <div class="profile-detail-row">
              <span class="profile-detail-label">{rows[2][0]}</span>
              <span class="profile-detail-value">{rows[2][1]}</span>
            </div>
          </div>
          <p class="profile-note">{L["profile_note"]}</p>
        </div>'''
    out = out.replace(profile_old, profile_new, 1)

    # Voicebank grid (each value/label block)
    vb_swaps = [
        ('<div class="voice-stat-value"><span class="vb-type">JA VCV&amp;CVVC</span></div>\n            <div class="voice-stat-label">语言·形式</div>',
         f'<div class="voice-stat-value"><span class="vb-type">{L["voicebank_grid"][0][0]}</span></div>\n            <div class="voice-stat-label">{L["voicebank_grid"][0][1]}</div>'),
        ('<div class="voice-stat-value">B3</div>\n            <div class="voice-stat-label">音阶（单音阶）</div>',
         f'<div class="voice-stat-value">{L["voicebank_grid"][1][0]}</div>\n            <div class="voice-stat-label">{L["voicebank_grid"][1][1]}</div>'),
        ('<div class="voice-stat-value">G2~C5</div>\n            <div class="voice-stat-label">推荐音域</div>',
         f'<div class="voice-stat-value">{L["voicebank_grid"][2][0]}</div>\n            <div class="voice-stat-label">{L["voicebank_grid"][2][1]}</div>'),
        ('<div class="voice-stat-value">HiFi类引擎</div>\n            <div class="voice-stat-label">推荐引擎</div>',
         f'<div class="voice-stat-value">{L["voicebank_grid"][3][0]}</div>\n            <div class="voice-stat-label">{L["voicebank_grid"][3][1]}</div>'),
    ]
    for old, new in vb_swaps:
        out = out.replace(old, new, 1)

    # Download accordion 1 (GitHub)
    gh_old = '''                <p class="accordion-desc">官方发布页面，获取最新版本</p>
                <a href="https://github.com/Heigao-Clank/kuro-voicebank/releases#release-V1" target="_blank" class="accordion-link">前往 GitHub V1 Release</a>'''
    gh_new = f'''                <p class="accordion-desc">{L["download_steps"][0][3]}</p>
                <a href="https://github.com/Heigao-Clank/kuro-voicebank/releases#release-V1" target="_blank" class="accordion-link">{L["download_steps"][0][4]}</a>'''
    out = out.replace(gh_old, gh_new, 1)
    cp_old = '''<button type="button" class="install-copy" aria-label="复制命令" title="复制命令">'''
    cp_new = f'''<button type="button" class="install-copy" aria-label="{L["install_label"]}" title="{L["install_title"]}">'''
    out = out.replace(cp_old, cp_new, 1)
    # Bowlroll
    br_old = '''                <p class="accordion-desc">日本文件分享服务</p>
                <span class="accordion-soon">二零二六年四月内将发布</span>'''
    br_new = f'''                <p class="accordion-desc">{L["download_steps"][1][3]}</p>
                <span class="accordion-soon">{L["download_steps"][1][4]}</span>'''
    out = out.replace(br_old, br_new, 1)
    # Cloud storage
    cs_old = '''                <span class="accordion-name">网盘下载</span>'''
    cs_new = f'''                <span class="accordion-name">{L["download_steps"][2][2]}</span>'''
    out = out.replace(cs_old, cs_new, 1)
    cs_old2 = '''                <p class="accordion-desc">备用下载方式</p>'''
    cs_new2 = f'''                <p class="accordion-desc">{L["download_steps"][2][3]}</p>'''
    out = out.replace(cs_old2, cs_new2, 1)
    out = out.replace('class="accordion-link">123云盘</a>', f'class="accordion-link">{L["download_steps"][2][4]}</a>', 1)
    out = out.replace('密码：<code', f'{L["pass_label"]}<code', 1)
    out = out.replace('this.title=\'已复制\'', f'this.title=\'{L["install_copied"]}\'', 1)
    out = out.replace('title="点击复制"', f'title="{L["copy_tooltip"]}"', 1)

    # Guidelines section: 3 cards
    allowed_old = '''              <div class="guideline-title">允许的事项</div>
            </div>
            <ul class="guideline-list">
              <li>个人非商业用途的创作</li>
              <li>视频投稿、直播、收益化（同人范围内）</li>
              <li>同人周边制作与销售（个人活动）</li>
              <li>二次创作（翻唱、Remix 等）</li>
              <li>不以角色名义使用（通用素材）</li>
              <li>AI 辅助后期处理（修音/混音）</li>
              <li>仅限本地私有模型训练（禁止外传）</li>
              <li>不署名（署名可选）</li>
            </ul>'''
    allowed_items = '\n'.join(f'              <li>{x}</li>' for x in L['allowed_items'])
    allowed_new = f'''              <div class="guideline-title">{L["allowed_title"]}</div>
            </div>
            <ul class="guideline-list">
{allowed_items}
            </ul>'''
    out = out.replace(allowed_old, allowed_new, 1)

    prohibited_old = '''              <div class="guideline-title">禁止的事项</div>
            </div>
            <ul class="guideline-list">
              <li class="no">分发原始音频样本（.wav 文件）</li>
              <li class="no">打包进收费产品</li>
              <li class="no">伪造制作者信息</li>
              <li class="no">公开训练/分发 AI 模型</li>
              <li class="no">用于违反法律法规的内容</li>
              <li class="no">正式商业用途（需单独授权）</li>
            </ul>'''
    prohibited_items = '\n'.join(f'              <li class="no">{x}</li>' for x in L['prohibited_items'])
    prohibited_new = f'''              <div class="guideline-title">{L["prohibited_title"]}</div>
            </div>
            <ul class="guideline-list">
{prohibited_items}
            </ul>'''
    out = out.replace(prohibited_old, prohibited_new, 1)

    contact_old = '''              <div class="guideline-title">需要联系作者</div>
            </div>
            <ul class="guideline-list">
              <li class="ask">正式商业场景使用</li>
              <li class="ask">企业主导的 PR/广告</li>
              <li class="ask">虚拟主播（Vtuber）皮套</li>
              <li class="ask">游戏内置语音</li>
              <li class="ask">音乐被收录至商业平台</li>
              <li class="ask">任何不确定的情况</li>
            </ul>'''
    contact_items = '\n'.join(f'              <li class="ask">{x}</li>' for x in L['contact_items'])
    contact_new = f'''              <div class="guideline-title">{L["contact_title"]}</div>
            </div>
            <ul class="guideline-list">
{contact_items}
            </ul>'''
    out = out.replace(contact_old, contact_new, 1)

    # Protocol tabs: ensure active class on the right language tab
    if L['lang'] == 'en':
        out = out.replace('<button class="protocol-tab active" data-lang="zh">中文</button>',
                          '<button class="protocol-tab" data-lang="zh">中文</button>', 1)
        out = out.replace('<button class="protocol-tab" data-lang="en">English</button>',
                          '<button class="protocol-tab active" data-lang="en">English</button>', 1)
    elif L['lang'] == 'jp':
        out = out.replace('<button class="protocol-tab active" data-lang="zh">中文</button>',
                          '<button class="protocol-tab" data-lang="zh">中文</button>', 1)
        out = out.replace('<button class="protocol-tab" data-lang="jp">日本語</button>',
                          '<button class="protocol-tab active" data-lang="jp">日本語</button>', 1)

    # FAQ section
    faq_old = '''        <div class="faq-list">
          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: 声库怎么用？</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                OpenUTAU 直接导入，推荐 HiFi类引擎。
              </div>
            </div>
          </div>

          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: 商用相关？</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                个人同人活动（发视频、卖周边等）不算商用。企业合作另谈。
              </div>
            </div>
          </div>

          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: 要署名吗？</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                不强制，标注的话非常感谢。
              </div>
            </div>
          </div>

          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: 能当普通素材用吗？</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                可以，不需要以角色名义。
              </div>
            </div>
          </div>

          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: AI 呢？</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                修音混音随意。本地私有模型训练允许，但严禁公开分发或用于训练公共 AI。
              </div>
            </div>
          </div>

          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: 同人要报告吗？</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                不用。
              </div>
            </div>
          </div>

          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: 不确定？</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                不给作者和角色惹麻烦就 OK，特殊情况直接联系。
              </div>
            </div>
          </div>
        </div>'''
    faq_items = '\n\n'.join(
        f'''          <div class="faq-item">
            <div class="faq-question" onclick="toggleFaq(this)">
              <span>Q: {q}</span>
              <div class="faq-icon"></div>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-content">
                {a}
              </div>
            </div>
          </div>''' for q, a in L['faq_pairs']
    )
    faq_new = f'''        <div class="faq-list">
{faq_items}
        </div>'''
    out = out.replace(faq_old, faq_new, 1)

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
        'self': 'index-en.html',
        'title': 'Shang Wei Yin Kousei | UTAU Voicebank',
        'description': 'Shang Wei Yin Kousei free UTAU Japanese voicebank (JA VCV&amp;CVVC). Wolf furry character with facial markings & twin tails. Great for covers and fan creation. Created by Heigao.',
        'og_desc': 'UTAU voicebank Shang Wei Yin Kousei — JA VCV&amp;CVVC Japanese single-scale library. Recommended engine: HiFi-class engine. Free to download for covers and fan creation.',
        'brand': 'Shang Wei Yin Kousei',
        'bg': ['SHANG WEI YIN KURO SHANG WEI YIN KURO SHANG WEI YIN KURO ',
               'UTAU • JA VCV&amp;CVVC UTAU • JA VCV&amp;CVVC ',
               'THANK YOU FOR USING THANK YOU FOR USING '],
        'nav': ['Voice Demo', 'Profile', 'Voice Info', 'Download', 'Guidelines', 'FAQ', 'Contact'],
        'side_nav': {'home': 'Home', 'demo': 'Voice Demo', 'profile': 'Profile', 'voicebank': 'Voice Info',
                     'download': 'Download', 'guidelines': 'Guidelines', 'faq': 'FAQ',
                     'contact': 'Contact', 'site': 'Personal Website'},
        'hero_alt': 'Shang Wei Yin Kousei',
        'hero_caption': 'Art · Heigao',
        'hero_title': 'Shang Wei Yin Kousei',
        'hero_subtitle': 'UTAU Japanese voicebank · <span class="vb-type">JA VCV&amp;CVVC</span>',
        'hero_desc': 'Twin-tailed Wolf Furry · Facial Markings<br><span class="text-muted">Independent sub-entity of an unknown extraterrestrial being</span>',
        'hero_btn1': 'Download',
        'hero_btn2': 'Guidelines',
        'hero_aria': 'Voice specifications',
        'tally_label': ['Format', 'Pitch (Single)', 'Best Range', 'Engine'],
        'tally_value': ['JA VCV&amp;CVVC', 'B3', 'G2~C5', 'HiFi-class engine'],
        'demo_title': 'Voice Demo',
        'demo_sub': 'Listen to the voicebank',
        'profile_title': 'Character Profile',
        'profile_sub': 'Details and personality',
        'profile_name': 'Shangwei Yin Kousei',
        'profile_meta': 'Wolf (Furry) <span class="sep">·</span> Approx. 17 <span class="sep">·</span> 168 cm',
        'profile_flavor': '&ldquo;One of the independent sub-entities of an unknown extraterrestrial being. Prone to drowsiness, actions often driven by unconsciousness. Facial markings and twin tails are natural features that change according to their state.&rdquo;',
        'profile_rows': [('Voice', 'Confident, Innocent'),
                          ('Features', 'Markings, twin tails (changes with state)'),
                          ('Likes', 'Watermelon')],
        'profile_note': '※ Other character details may be freely added for fan creation',
        'voicebank_title': 'Voice Information',
        'voicebank_sub': 'Technical specifications',
        'voicebank_grid': [('JA VCV&amp;CVVC', 'Format'),
                           ('B3', 'Pitch (Single)'),
                           ('G2~C5', 'Best Range'),
                           ('HiFi-class engine', 'Engine')],
        'download_title': 'Download',
        'download_sub': 'Get the latest version',
        'download_steps': [
            ('primary', '01', 'GitHub', 'Official page for the latest updates.', 'Go to GitHub V1 Release'),
            ('warm', '02', 'Bowlroll', 'Alternative mirror (Japan).', 'Coming in April 2026'),
            ('secondary', '03', 'Cloud Storage', 'Alternative download.', 'Google Drive', '123 Cloud', 'star'),
        ],
        'install_label': 'Copy command',
        'install_title': 'Copy command',
        'install_copied': 'Copied',
        'copy_tooltip': 'Click to copy',
        'pass_label': 'Password: ',
        'guidelines_title': 'Usage Guidelines',
        'guidelines_sub': 'Usage Guidelines',
        'allowed_title': 'Allowed',
        'allowed_items': ['Personal non-commercial use',
                          'Video uploads, streaming &amp; monetization (within fan scope)',
                          'Fan merchandise (personal activity)',
                          'Derivative works (covers, remix, etc.)',
                          'Use as a general sound resource',
                          'AI-assisted post-processing (pitch / mix)',
                          'Local, non-public private training only',
                          'Optional attribution'],
        'prohibited_title': 'Prohibited',
        'prohibited_items': ['Distribution of original audio (.wav)',
                             'Packaging into paid products',
                             'Falsifying creator info',
                             'Public distribution of trained AI models',
                             'Content that breaks the law',
                             'Official commercial use (requires approval)'],
        'contact_title': 'Contact',
        'contact_items': ['Official commercial scenarios',
                          'Corporate-led PR / advertising',
                          'VTuber avatar use',
                          'In-game voice use',
                          'Music on commercial platforms',
                          'Any uncertain cases'],
        'faq_title': 'FAQ',
        'faq_sub': 'FAQ',
        'faq_pairs': [
            ('How do I use the voicebank?', 'Import directly into OpenUTAU. Recommended engine: HiFi-class.'),
            ('Commercial use?', 'Personal / fan activity is not commercial. Enterprise use is — please contact.'),
            ('Required credit?', 'No. Credit is appreciated but optional.'),
            ('Can I use it as plain audio?', 'Yes. No character attribution required.'),
            ('AI usage?', 'Pitch / mix processing is OK. Local private training is OK, but public distribution or use for training public AI is forbidden.'),
            ('Do I need to report fan works?', 'No.'),
            ('Unsure about something?', 'If it does not cause trouble for the author or character, you should be fine. Otherwise, contact the author.'),
        ],
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
        'self': 'index-jp.html',
        'title': '熵尾音 咬青 | UTAU Voicebank',
        'description': 'UTAU音源「熵尾音 咬青」JA VCV&amp;CVVC 日语音阶声库免费下载。面纹と二尾の狼獣人キャラクター。同人・カバー・二次創作に。制作：黒篙（Heigao）。',
        'og_desc': 'UTAU音源「熵尾音 咬青」- JA VCV&amp;CVVC 日语音阶声库、推奨エンジン HiFiUtau、カバーと二次創作用に無料ダウンロード可能。',
        'brand': '熵尾音 咬青',
        'bg': ['熵尾音 こうせい 熵尾音 こうせい 熵尾音 こうせい ',
               'UTAU • JA VCV&amp;CVVC UTAU • JA VCV&amp;CVVC ',
               'ご利用ありがとうございます '],
        'nav': ['试听', 'プロフィール', '音源情報', 'ダウンロード', '規約', 'FAQ', '連絡先'],
        'side_nav': {'home': 'ホーム', 'demo': '试听', 'profile': 'プロフィール',
                     'voicebank': '音源情報', 'download': 'ダウンロード', 'guidelines': '規約',
                     'faq': 'よくある質問', 'contact': '連絡先', 'site': '個人サイト'},
        'hero_alt': '熵尾音 咬青',
        'hero_caption': 'イラスト · 黒篙',
        'hero_title': '熵尾音 咬青',
        'hero_subtitle': 'UTAU 日本語音源 · <span class="vb-type">JA VCV&amp;CVVC</span>',
        'hero_desc': '二尾の狼獣人 · 顔面の紋様<br><span class="text-muted">未知の天外来物の独立サブエンティティ</span>',
        'hero_btn1': 'ダウンロード',
        'hero_btn2': '規約',
        'hero_aria': '音源仕様',
        'tally_label': ['形式', '音階（単音階）', '推奨音域', '推奨エンジン'],
        'tally_value': ['JA VCV&amp;CVVC', 'B3', 'G2~C5', 'HiFiクラスエンジン'],
        'demo_title': '试听デモ',
        'demo_sub': 'ボイスバンクを聴く',
        'profile_title': 'プロフィール',
        'profile_sub': 'キャラクター紹介',
        'profile_name': '熵尾音 咬青',
        'profile_meta': '狼獣人 <span class="sep">·</span> 約17歳 <span class="sep">·</span> 168cm',
        'profile_flavor': '「未知の天外来物の独立したサブエンティティの一つ。居眠りしやすく、行動は無意識に動かされることが多い。顔面の紋様と二尾は天生形成で、状態に応じて変化する。」',
        'profile_rows': [('声質', '自信に満ち、純真'),
                          ('特徴', '紋様、二尾（状態に応じて変化）'),
                          ('好物', 'スイカ')],
        'profile_note': '※ その他の設定は自由に補足・二次創作に使用可能',
        'voicebank_title': '音源情報',
        'voicebank_sub': '仕様',
        'voicebank_grid': [('JA VCV&amp;CVVC', '形式'),
                           ('B3', '音階（単音階）'),
                           ('G2~C5', '推奨音域'),
                           ('HiFiクラスエンジン', '推奨エンジン')],
        'download_title': 'ダウンロード',
        'download_sub': '最新版を取得',
        'download_steps': [
            ('primary', '01', 'GitHub', '公式リリースページです。', 'GitHub V1 Release へ'),
            ('warm', '02', 'Bowlroll', '日本の配布サービス。', '2026年4月中に公開予定'),
            ('secondary', '03', 'クラウド', '代替ダウンロード。', 'Google Drive', '123クラウド', 'star'),
        ],
        'install_label': 'コマンドをコピー',
        'install_title': 'コマンドをコピー',
        'install_copied': 'コピーしました',
        'copy_tooltip': 'クリックしてコピー',
        'pass_label': 'パスワード：',
        'guidelines_title': '使用規約',
        'guidelines_sub': '利用規約',
        'allowed_title': '許可される事項',
        'allowed_items': ['個人的な非商用利用',
                          '動画投稿・配信・収益化（同人範囲内）',
                          '同人グッズ制作と販売（個人活動）',
                          '二次創作（カバー、Remix など）',
                          '汎用素材としての利用',
                          'AI によるポスト処理（ピッチ／ミックス）',
                          'ローカル限定・非公開の個人訓練のみ',
                          'クレジットは任意'],
        'prohibited_title': '禁止される事項',
        'prohibited_items': ['原音ファイル（.wav）の配布',
                             '有料製品への同梱',
                             '制作者情報の偽装',
                             '学習済み AI モデルの公開配布',
                             '法律違反となるコンテンツ',
                             '正式な商用利用（要許諾）'],
        'contact_title': '作者への相談',
        'contact_items': ['正式な商用利用',
                          '企業主体の PR / 広告',
                          'VTuber モデルとしての使用',
                          'ゲーム内の音声使用',
                          '商業プラットフォームへの楽曲収録',
                          '判断に迷うケース'],
        'faq_title': 'よくある質問',
        'faq_sub': 'FAQ',
        'faq_pairs': [
            ('使い方は？', 'OpenUTAU に直接インポートしてください。推奨エンジンは HiFi クラスです。'),
            ('商用利用は？', '個人・同人活動は商用ではありません。企業利用は事前にご連絡ください。'),
            ('クレジットは？', '必須ではありません。任意です。'),
            ('一般素材として使える？', 'はい。キャラクター名義なしで使えます。'),
            ('AI は？', 'ピッチ／ミックス処理は OK。ローカル限定・非公開の個人訓練は OK ですが、学習済みモデルの公開配布や公共 AI への学習利用は禁止です。'),
            ('同人の報告は？', '不要です。'),
            ('判断に迷ったら？', '作者とキャラクターに迷惑をかけなければ基本的に問題ありません。迷う場合はご連絡ください。'),
        ],
        'contact_section_title': '連絡先',
        'contact_section_sub': 'お問い合わせ',
        'contact_field': [
            ('Email', 'heigao75@qq.com', 'mailto:heigao75@qq.com'),
            ('Twitter/X', '@heigao_tickle', 'https://twitter.com/heigao_tickle'),
            ('Bilibili', '黒篙', 'https://space.bilibili.com/695724697'),
            ('個人サイト', 'heigao.me', 'https://heigao.me/'),
        ],
        'footer_title': '熵尾音 咬青 UTAU Voicebank',
        'footer_cr': '© 2026 黒篙 All Rights Reserved.',
    }


def main():
    en = apply(src, locale_en())
    (ROOT / 'index-en.html').write_text(en)
    print('EN size:', len(en))
    jp = apply(src, locale_jp())
    (ROOT / 'index-jp.html').write_text(jp)
    print('JP size:', len(jp))


if __name__ == '__main__':
    main()