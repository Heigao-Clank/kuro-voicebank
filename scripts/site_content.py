"""Render voicebank information, usage terms and FAQs from the three bundled guides."""
from html import escape
import re


FILES = {'zh': 'Readme.txt', 'en': 'Readme_EN.txt', 'jp': 'Readme_JP.txt'}
PAGE = {'zh': 'index.html', 'en': 'index-en.html', 'jp': 'index-jp.html'}
LANG = {'zh': 'zh-CN', 'en': 'en', 'jp': 'ja'}
COPY = {
    'zh': {
        'name': '熵尾音 咬青', 'caption': '插图 · 黑篙', 'subtitle': 'UTAU 日语音源',
        'hero': ('双尾狼兽人 · 面纹', '来自宇宙，是某个未知存在的独立子体之一。'),
        'description': '熵尾音 咬青是来自宇宙的双尾狼兽人。日语 UTAU 声库收录软声、真声和假声，采用 CVVC 与 VCV 格式。提供试听、声库下载及分版本使用协议。',
        'guide_title': 'V1.1 使用协议', 'archive': '查看 V1 使用协议', 'actions': ('下载音源', '使用协议'),
        'notes_title': 'V1.1 声线说明',
        'recorded': '软声（_S）录于 {软声}，真声（_O）录于 {真声}，假声（_F）录于 {假声}。',
        'main_setting': '默认声线（Main）在 {low} 及以下使用真声，从 {high} 起切换为假声。',
        'pitch': '录制音高', 'style': '声线', 'basic': '基础信息', 'intro': '角色简介',
        'buttons': ('允许的事项', '禁止的事项', '需事先取得授权'),
        'download': '公开下载：V1', 'mirror': 'V1 备用下载', 'soon': '暂无下载链接',
        'summary': [
            ['个人可自行投稿、领取平台创作激励及比赛奖金；角色名和作者名均可选择是否署名。',
             '可承接指定本音源的商业歌曲委托。交付的咬青人声须直接用本 UTAU 音源调声、渲染。',
             '个人创作可用已渲染的人声作 AI 参考，本地或在线生成歌声、语音。在线处理或生成须明确排除用提交的音频训练模型；用原始录音或渲染人声训练模型，仅限本人在本地进行非公开的调声实验。',
             '上述个人音频可单独或随作品上传，供非商业分享。可修改并单独分享 oto.ini 和 .frq，分享时不得附带声库录音样本。',
             '个人可以制作和销售同人周边，包括使用自绘图案的商品。',
             '官方立绘可用于使用本音源的作品封面或视频；用于专辑封面时仅限非付费专辑，裁切或改色亦同。'],
            ['分发原始录音或转码副本，或将本音源打包进收费产品。',
             '向他人提供二次声库、模型权重或可复现咬青音色的特征数据；将本音源或二次声库接入公开 AI 服务。',
             '使用本音源开发或训练商业 AI 产品，或交付模型生成、转换的咬青委托人声。',
             '冒认制作者，或制作、传播协议所禁止的违法、仇恨、歧视等内容。'],
            ['通过发行商发行音乐、收录于商业唱片或付费专辑、商业游戏用曲及游戏内置语音。',
             '将角色设定或形象用于企业宣传、量产商品或虚拟主播的出镜形象。',
             '专辑封面以外的商品直接使用官方立绘或其裁切、改色版本。']],
    },
    'en': {
        'name': 'Shang Wei Yin Kousei', 'caption': 'Art · Heigao', 'subtitle': 'Japanese UTAU voicebank',
        'hero': ('Twin-tailed wolf with facial markings', 'From outer space, one of the independent offshoots of an unknown entity.'),
        'description': 'Meet Kousei, a twin-tailed wolf from outer space. Hear his three Japanese UTAU voice styles, explore the CVVC and VCV voicebank, and find downloads and terms for each version.',
        'guide_title': 'V1.1 Terms of Use', 'archive': 'Read the V1 terms', 'actions': ('Download voicebank', 'Usage guidelines'),
        'notes_title': 'V1.1 voice styles',
        'recorded': 'Soft (_S) was recorded at {Soft}, Original (_O) at {Original}, and Falsetto (_F) at {Falsetto}.',
        'main_setting': 'The default setting (Main) uses Original at {low} and below, and switches to Falsetto at {high}.',
        'pitch': 'Recording pitches', 'style': 'Voice', 'basic': 'Basic Information', 'intro': 'Character Description',
        'buttons': ('Permitted uses', 'Prohibited uses', 'Prior permission required'),
        'download': 'Public download: V1', 'mirror': 'V1 download mirrors', 'soon': 'Download link not yet available',
        'summary': [
            ['Individual creators may upload directly to platforms and accept creator rewards or competition prizes. Both character and creator credits are optional.',
             'You may take paid commissions for commercial songs using this voicebank. Tune and render the Kousei vocals you deliver directly with the UTAU voicebank.',
             'For personal projects, you may use rendered vocals as reference audio to generate singing or speech locally or online. Online services must explicitly exclude submitted audio from training under their terms or your settings. You may train a model on the original recordings or rendered vocals only on your own device for your own private vocal-tuning experiments.',
             'You may upload those vocals for noncommercial sharing, alone or as part of a work. You may modify and share oto.ini and .frq files separately, without including any voicebank recordings.',
             'As an individual, you may make and sell fan merchandise, including items featuring your own artwork.',
             'You may show official artwork on the cover of a work made with the voicebank or in its video. For album covers, this applies only to albums released free of charge, including cropped or recolored artwork.'],
            ['Redistributing original recordings or converted copies, or bundling the voicebank with a paid product.',
             'Sharing derivative voicebanks, model weights or features that can reproduce Kousei’s timbre, or connecting the voicebank or a derivative voicebank to a public AI service.',
             'Developing or training commercial AI products with the voicebank, or delivering model-generated or converted Kousei vocals on commission.',
             'Falsely claiming authorship or creating or spreading unlawful, hateful or discriminatory content prohibited by the terms.'],
            ['Releases through a distributor, placement on commercial records or paid albums, music for commercial games, and in-game voice audio.',
             'Using Kousei’s character concept or likeness for corporate promotions, mass-produced merchandise or a VTuber’s on-screen persona.',
             'Using official artwork, including cropped or recolored versions, on merchandise other than album covers.']],
    },
    'jp': {
        'name': '熵尾音 こうせい', 'caption': 'イラスト · 黒篙', 'subtitle': 'UTAU日本語音源',
        'hero': ('顔に模様のある、2本のしっぽを持つ狼獣人', '宇宙からやってきた、ある未知の存在に由来する独立した分体のひとつです。'),
        'description': '宇宙からやってきた、2本のしっぽを持つ狼獣人「熵尾音 こうせい」。ソフト・地声・裏声を収録した日本語UTAU音源（CVVC・VCV）の試聴、ダウンロード、バージョン別の利用規約を掲載しています。',
        'guide_title': 'V1.1 の利用規約', 'archive': 'V1の利用規約を読む', 'actions': ('音源ダウンロード', '利用規約'),
        'notes_title': 'V1.1 の声色について',
        'recorded': 'ソフト（_S）は{ソフト}、地声（_O）は{地声}、裏声（_F）は{裏声}で収録しました。',
        'main_setting': '標準設定（Main）では、{low}以下で地声を使い、{high}から裏声に切り替わります。',
        'pitch': '収録音高', 'style': '声の特徴', 'basic': '基本情報', 'intro': 'キャラクター紹介',
        'buttons': ('許諾不要の利用', '禁止事項', '事前に作者の許諾が必要な利用'),
        'download': '配布中の音源：V1', 'mirror': 'V1のミラー配布先', 'soon': 'ダウンロードリンクは準備中です',
        'summary': [
            ['個人での直接投稿、投稿先の奨励金やコンテスト賞金の受け取りができます。キャラクター名と制作者名の表記はいずれも任意です。',
             '本音源を指定した商用楽曲の有償依頼も受けられます。納品するこうせいの声は、このUTAU音源で直接調声して書き出してください。',
             '個人の創作では、書き出した音声を参照してローカルでもオンラインでも歌声や話し声を生成できます。オンラインでの処理・生成には、規約または設定で送信音声を学習対象から明確に除外するサービスを使ってください。収録音声や書き出した音声を使ったモデル学習は、自分の端末で行う非公開の調声実験に限ります。',
             '上記の音声は非商用での共有を目的に、単体でも作品の一部としても投稿できます。oto.iniや.frqは編集して単独で配布できます。音源の収録音声は同梱しないでください。',
             '個人の活動の範囲で、自作のイラストを使ったものを含め、同人グッズを制作・販売できます。',
             '公式立ち絵は本音源を使った作品の表紙や動画に使用できます。アルバムのジャケットへの使用は無償配布のアルバムに限り、切り抜き・色変更にも同じ条件が適用されます。'],
            ['収録音声や形式を変換した複製の再配布、有料製品への音源の同梱。',
             '二次音源・モデルの重み・こうせいの声質を再現できる特徴量の第三者への提供、本音源や二次音源の公開AIサービスへの接続。',
             '本音源を使った商用AI製品の開発・学習、依頼作品でこうせいの声をモデルで生成・変換して納品すること。',
             '制作者の詐称や、法令違反・憎悪・差別など、規約で禁止されている内容の制作・拡散。'],
            ['ディストリビューター経由のリリース、商業盤・有料アルバムへの収録、商用ゲームへの楽曲提供、ゲームへのボイスの組み込み。',
             'キャラクターの設定や姿を企業の宣伝、量産グッズ、VTuberの配信用アバターに使うこと。',
             'アルバムのジャケット以外の商品に公式立ち絵を使うこと。切り抜きや色変更を加えたものも含みます。']],
    },
}


def once(pattern, replacement, text):
    updated, count = re.subn(pattern, lambda m: replacement(m) if callable(replacement) else replacement, text, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one match for {pattern}, got {count}')
    return updated


def elements(text, tag, cls, values):
    """Replace the contents of a known set of sibling elements, retaining their attributes."""
    pattern = rf'(<{tag} class="{cls}"[^>]*>).*?(</{tag}>)'
    if len(re.findall(pattern, text, flags=re.S)) != len(values):
        raise ValueError(f'Unexpected number of {cls} elements')
    it = iter(values)
    return re.sub(pattern, lambda m: m[1] + next(it) + m[2], text, flags=re.S)


def field_value(line):
    return re.split(r'[:：]', line, maxsplit=1)[1].strip()


def guide_html(text):
    sections = []
    for block in re.split(r'\n\s*\n', text.strip()):
        if block == '---':
            sections.append('<hr>')
            continue
        paragraph = []
        for line in block.splitlines():
            line = line.strip()
            if re.match(r'^(?:#+ |■ |🔷|◆ |【|× |△ |⚪)', line):
                if paragraph:
                    sections.append('<p>'+'<br>'.join(paragraph)+'</p>')
                    paragraph = []
                sections.append('<h3>'+escape(line.lstrip('# '))+'</h3>')
            else:
                safe = escape(line)
                safe = re.sub(r'https?://[A-Za-z0-9_./#?=&%-]+',lambda m:f'<a href="{m[0]}">{m[0]}</a>',safe)
                paragraph.append(safe)
        if paragraph:
            sections.append('<p>'+'<br>'.join(paragraph)+'</p>')
    return '\n'.join(sections)


def read_guide(root, lang):
    text = (root / FILES[lang]).read_text(encoding='utf-8')
    info = COPY[lang]
    basic = text.split(f'【{info["basic"]}】\n', 1)[1].split('\n\n', 1)[0].splitlines()
    profile = text.split(f'【{info["intro"]}】\n', 1)[1].split('\n---', 1)[0].strip().split('\n\n')
    if len(basic) != 6 or len(profile) != 3:
        raise ValueError(f'Check {lang} profile structure')
    specs = next(block for block in text.split('\n\n') if re.search(r'^(?:形式：|Type: )JA ', block, re.M)).splitlines()
    fmt, pitches, comfortable, voice = [field_value(line) for line in specs[1:]]
    faq = re.findall(r'^Q: ([^\n]+)\nA: ([^\n]+(?:\n +[^\n]+)*)', text, re.M)
    if not faq:
        raise ValueError(f'Missing {lang} FAQ')
    main = re.search(r'^\s*(Main[:：].+)$',text,re.M)[1]
    return dict(main=main, basic=[field_value(s) for s in basic], profile=profile, faq=faq, fmt=fmt, pitches=pitches,
                comfortable=comfortable, voice=voice, full=guide_html(text))


def section(page, name, update):
    return once(rf'(<section [^>]*id="{name}"[^>]*>)(.*?)(</section>)', lambda m: m[1]+update(m[2])+m[3], page)


def update_page(page, lang, guides):
    c, g = COPY[lang], guides[lang]
    e = escape
    def hero(s):
        s = elements(s, 'p', 'hero-eyebrow', ['UTAU VOICEBANK · V1.1'])
        s = elements(s, 'h1', 'hero-title', [e(c['name'])])
        s = elements(s, 'p', 'hero-subtitle', [e(c['subtitle'])+' · <span class="vb-type">'+e(g['fmt'])+'</span>'])
        s = elements(s, 'p', 'hero-description', [e(c['hero'][0])+'<br><span class="text-muted">'+e(c['hero'][1])+'</span>'])
        s = elements(s, 'p', 'hero-visual-text', [e(c['caption'])])
        s = once(r'(<img [^>]*?alt=")[^"]*("[^>]*class="hero-character")', lambda m:m[1]+e(c['name'])+m[2], s)
        for kind, label in zip(('primary','secondary'),c['actions']):
            s = once(rf'(<a [^>]*class="btn btn-{kind}"[^>]*>.*?</svg>)\s*[^<]*(</a>)',
                     lambda m:m[1]+' '+e(label)+m[2],s)
        s = elements(s,'dt','hero-tally-label',labels)
        return elements(s,'dd','hero-tally-value',values)

    labels = [e(v) for v in {'zh': ('语言·形式',c['pitch'],'舒适音域','推荐引擎'),
                             'en': ('Format',c['pitch'],'Comfortable range','Engine'),
                             'jp': ('形式',c['pitch'],'得意音域','推奨エンジン')}[lang]]
    recorded = dict(part.strip().rsplit(maxsplit=1) for part in re.split(r'[,、]', g['pitches']))
    if len(recorded) != 3:
        raise ValueError(g['pitches'])
    values = ['<span class="vb-type">'+e(g['fmt'])+'</span>', ' / '.join(recorded.values()), e(g['comfortable']),'HiFiUTAU']
    page = section(page,'hero',hero)

    def profile(s):
        name, age, birth, gender, height, species = g['basic']
        s = elements(s,'h3','profile-name',[e(name)])
        birth_label={'zh':'生日','en':'Birthday: ','jp':'誕生日：'}[lang]
        meta = ' <span class="sep">·</span> '.join(e(v) for v in (species, gender, age, birth_label+birth, height))
        s = elements(s,'p','profile-sub',[meta])
        s = elements(s,'blockquote','profile-flavor',['<p>'+e(g['profile'][0])+'</p>'])
        details = [block.split('\n',1) for block in g['profile'][1:]]
        features,likes,feature_text,fruit = {
            'zh': ('特征','喜好','面纹、双尾（随状态变化）','西瓜'),
            'en': ('Features','Likes','Facial markings and twin tails that change with his state','Watermelon'),
            'jp': ('特徴','好物','状態に応じて変化する顔の模様と2本のしっぽ','スイカ')
        }[lang]
        s = elements(s,'span','profile-detail-label',[e(x) for x in (c['style'],features,likes,*(title.rstrip(':：') for title,_ in details))])
        return elements(s,'span','profile-detail-value',[e(x) for x in (g['voice'],feature_text,fruit,*(v for _,v in details))])
    page = section(page,'profile',profile)

    def download(s):
        low, high = re.findall(r'[A-G][#b]?\d+', g['main'])
        lines = [c['recorded'].format_map(recorded), c['main_setting'].format(low=low, high=high)]
        s = elements(s, 'h3', 'voice-notes-title', [e(c['notes_title'])])
        s = elements(s, 'p', 'voice-usage', ['<br>'.join(map(e, lines))])
        heading, link, bowl = {'zh': ('下载音源','前往 GitHub 下载 V1','日本文件分享服务'),
                              'en': ('Download','Download V1 on GitHub','Japanese file-sharing service.'),
                              'jp': ('ダウンロード','GitHubのV1配布ページへ','日本のファイル配布サービス。')}[lang]
        s = once(r'(<h2>).*?(</h2>)',lambda m:m[1]+e(heading)+m[2],s)
        s = once(r'(<a href="https://github.com/Heigao-Clank/kuro-voicebank/releases[^"]*"[^>]*>).*?(</a>)',lambda m:m[1]+e(link)+m[2],s)
        s = once(r'(<div class="section-title">\s*<h2>[^<]*</h2>\s*<p>).*?(</p>)',lambda m:m[1]+e(c['download'])+f' · <a href="assets/terms-v1.html#{lang}">'+e(c['archive'])+'</a>'+m[2],s)
        s=elements(s,'p','accordion-desc',[e(c['download']),e(bowl),e(c['mirror'])])
        s=elements(s,'span','accordion-soon',[e(c['soon'])])
        return s.replace('/releases#release-V1','/releases/tag/V1').replace('gh release download --repo','gh release download V1 --repo')
    page=section(page,'download',download)
    if lang == 'zh':
        page = page.replace('熵尾咬青 熵尾咬青 熵尾咬青 ', '熵尾音 咬青 熵尾音 咬青 熵尾音 咬青 ')
    def guidelines(s):
        title = {'zh':'使用协议','en':'Usage Guidelines','jp':'利用規約'}[lang]
        s = once(r'(<h2>).*?(</h2>)', lambda m:m[1]+title+m[2],s)
        s=once(r'(<div class="section-title">\s*<h2>[^<]*</h2>\s*<p>).*?(</p>)',
               lambda m:m[1]+e(c['guide_title'])+f' · <a href="assets/terms-v1.html#{lang}">'+e(c['archive'])+'</a>'+m[2], s)
        s=elements(s,'div','guideline-title',list(map(e,c['buttons'])))
        lists=[]
        for attr,items in zip(('', ' class="no"', ' class="ask"'), c['summary']):
            lists.append('\n'+'\n'.join(f'              <li{attr}>{e(item)}</li>' for item in items)+'\n            ')
        s=elements(s,'ul','guideline-list',lists)
        def panel(m):
            code=m[1]
            style='' if code==lang else ' hidden'
            return (f'<div class="protocol-content" id="protocol-{code}" lang="{LANG[code]}"{style}>\n'
                    f'            <div class="protocol-text">{guides[code]["full"]}</div>\n          </div>')
        s,count=re.subn(r'<div class="protocol-content" id="protocol-(zh|en|jp)"[^>]*>\s*<div class="protocol-text">.*?</div>\s*</div>',panel,s,flags=re.S)
        if count!=3: raise ValueError('Expected three complete protocol panels')
        return re.sub(r'<button class="protocol-tab(?: active)?" data-lang="(\w+)"[^>]*>',lambda m:
                      f'<button class="protocol-tab{" active" if m[1]==lang else ""}" data-lang="{m[1]}" type="button" aria-controls="protocol-{m[1]}" aria-pressed="{str(m[1]==lang).lower()}">',s)
    page=section(page,'guidelines',guidelines)
    def faq(s):
        items=[]
        for index,(question,answer) in enumerate(g['faq'], 1):
            answer='<br>'.join(e(line.strip()) for line in answer.splitlines())
            items.append(f'''          <details class="faq-item">
            <summary class="faq-question" aria-controls="faq-answer-{index}">
              <span>Q: {e(question)}</span>
              <span class="faq-icon"></span>
            </summary>
            <div class="faq-answer" id="faq-answer-{index}">
              <div class="faq-answer-content">{answer}</div>
            </div>
          </details>''')
        return once(r'(<div class="faq-list">).*?(</div>\s*</div>\s*)$', lambda m:m[1]+'\n'+'\n'.join(items)+'\n        '+m[2],s)
    page=section(page,'faq',faq)
    if lang != 'zh':
        page = section(page,'demo',lambda s: elements(s,'span','demo-card-desc',['エリート','レテノール','初音ミクの消失']))
        site_label={'en':'Personal website','jp':'個人サイト'}[lang]
        page=page.replace('个人网站',site_label)
    page=once(r'(<dl class="hero-tally" aria-label=")[^"]*(">)', lambda m:m[1]+{'zh':'音源规格','en':'Voicebank specifications','jp':'音源仕様'}[lang]+m[2],page)

    for key in ('name="description"', 'property="og:description"'):
        page=once(rf'(<meta {key} content=")[^"]*(">)',lambda m:m[1]+e(c['description'])+m[2],page)
    page=page.replace('https://kuro-voicebank.pages.dev/','https://kuro-utau.heigao.me/')
    page=re.sub(r'(hreflang="x-default" href="https://kuro-utau\.heigao\.me/)[^"]*',r'\1',page)
    return page


def render_pages(root, shells):
    guides = {lang: read_guide(root, lang) for lang in FILES}
    return {PAGE[lang]: update_page(shell, lang, guides) for lang, shell in shells.items()}
