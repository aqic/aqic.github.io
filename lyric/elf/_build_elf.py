# -*- coding: utf-8 -*-
import os
import glob
import re

# 基于脚本自身位置定位，便于在本目录内独立复用：
#   BASE = 本脚本所在目录 (elf)
#   DST  = 输出 HTML / 索引 / _map.py 到本目录
#   SRC  = 源歌词 txt 放在本目录下的 src/ 子目录（与脚本同级）
BASE = os.path.dirname(os.path.abspath(__file__))
DST = BASE
SRC = os.path.join(BASE, "src")
IMG = "elf.gif"
INDEX = "0-elf-index.html"

MARKS = "※★☆◇◆＊"
IDEOSP = "\u3000"

# ---- 歌曲元数据（已对照网上资料订正出处/制作）----
SONGS = [
    # ===== 专辑「élf ANIMATION SONG FILE」(KSCA-59134 / 2000-07-21) 收录顺序 14 首（+ 外链 1） =====
    dict(no=1, slug="everybrandnewday", src="elf-everybrandnewday.txt",
         title="Every Brand-new Day",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>TV アニメーション「下級生」オープニングテーマ",
         performer="安達まり",
         staff="作詞：藤林聖子<br>作曲：くにたけみゆき<br>編曲：高橋一之",
         zh=None),
    dict(no=2, slug="eternal", src="elf-enternal.txt",
         title="ETERNAL",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「ドラゴンナイト４」エンディングテーマ",
         performer="淺田葉子",
         staff="作詞：松本花奈<br>作曲・編曲：タダミツヒロ",
         zh=None),
    # ===== Reflain Blue =====
    dict(no=3, slug="face", src="elf-face.txt",
         title="FACES",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「この世の果てで恋を唄う少女 YU-NO」第３幕・第４幕 エンディングテーマ",
         performer="そのざき みえ（園崎未恵）",
         staff="作詞：六ツ見純代<br>作曲・編曲：坂本昌之",
         zh=None),
    # ===== ドラゴンナイト４ =====
    dict(no=4, slug="color", src="elf-color.txt",
         title="色づく頃に…",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「同級生２」TV 編集版　オープニングテーマ",
         performer="橘 ひかり",
         staff="作詞：山崎明子<br>作曲：岡崎律子<br>編曲：淡野保昌",
         zh=None),
    dict(no=5, slug="suki", src="elf-suki.txt",
         title="“好き”と言えたら…",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「エルフ版 下級生 ～あなただけを見つめて…」エンディングテーマ",
         performer="茶山莉子",
         staff="",
         zh=None),
    dict(no=6, slug="girlsbeup", src="elf-girlsbeup.txt",
         title="Girls be UP!",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>TV アニメーション「下級生」エンディングテーマ",
         performer="あっぷ²",
         staff="作詞：山崎明子<br>作曲：pap_lu<br>編曲：岩室晶子",
         zh=None),
    dict(no=7, slug="naze", src="elf-naze.txt",
         title="なぜ？",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「恋姫」エンディングテーマ",
         performer="寺田 はるひ",
         staff="",
         zh=None),
    # ===== ビ・ヨンド =====
    dict(no=8, slug="siawasenohana", src="elf-siawasenohana.txt",
         title="幸せの花束",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「ビ・ヨンド」エンディングテーマ",
         performer="そのざき みえ（園崎未恵）",
         staff="",
         zh=None),
    # ===== らいむいろ戦記譚 =====
    dict(no=9, slug="rureto", src="elf-rureto.txt",
         title="ルーレット・キャンドル",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「エルフ版 下級生」MUSIC GRAFFITI 特典",
         performer="Pure'（安達まり・茶山莉子・柳原みわ）",
         staff="",
         zh=None),
    dict(no=10, slug="seamoonlight", src="elf-seamoonlight.txt",
         title="Sea －月のあかり－",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「エルフ版 下級生」MUSIC GRAFFITI 特典",
         performer="菊地 由美",
         staff="",
         zh=None),
    # ===== TV アニメーション 下級生 =====
    dict(no=11, slug="tokimeki", src="elf-tokimeki.txt",
         title="トキメキの行方",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「エルフ版 下級生 ～あなただけを見つめて…」オープニングテーマ",
         performer="安達まり",
         staff="",
         zh=None),
    dict(no=12, slug="light", src="elf-light.txt",
         title="光のリング",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「同級生２」TV 編集版 EXTRA BOX 特典",
         performer="菊地 由美",
         staff="",
         zh=None),
    dict(no=13, slug="suki2", src="elf-su-ki.txt",
         title="すき",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「同級生２ Special 卒業生」エンディングテーマ",
         performer="寺田 はるひ",
         staff="",
         zh=None),
    dict(no=14, slug="voices", src="elf-voices.txt",
         title="VOICES",
         prov="アルバム「élf ANIMATION SONG FILE」収録<br>「この世の果てで恋を唄う少女 YU-NO」第１幕・第２幕 エンディングテーマ",
         performer="そのざき みえ（園崎未恵）",
         staff="",
         zh=None),
    # ===== 专辑未收录的单曲（按游戏分） =====
    # --- 同級生２ ---
    dict(no=15, slug="haru", src="elf-haru.txt",
         title="春を待つ季節",
         prov="Sega Saturn 版「同級生２」エンディングテーマ",
         performer="鳴澤 唯（CV：松下 美由紀）",
         staff="作詞：ドン・マッコウ<br>作・編曲：岩垂 德行",
         zh=None),
    dict(no=16, slug="natsu", src="elf-natsu.txt",
         title="夏色のシソデレラ",
         prov="PC Engine 版「同級生２」主題歌",
         performer="小野寺麻理子（田中美沙）／小野綾子（黒川さとみ）<br>笠原留美（仁科くるみ）／丹下 桜（鈴木美穂）",
         staff="作詞：溝口 功<br>作曲・編曲：岩垂德行",
         zh=None),
    dict(no=17, slug="onemoment", src="elf-onemoment.txt",
         title="One Moment（Vocal Version）",
         prov="「同級生II」",
         performer="寺尾友美",
         staff="",
         zh="elf-onemoment_中.txt"),
    dict(no=18, slug="sweetonyou", src="elf-sweetonyou.txt",
         title="Sweet on You（Vocal Version）",
         prov="「同級生II」",
         performer="寺尾友美",
         staff="",
         zh="elf-sweetonyou_中.txt"),
    # ===== エルフ版 下級生 =====
    # --- TV アニメーション 下級生 ---
    dict(no=19, slug="summergirl", src="elf-summergirl.txt",
         title="Summer Girl",
         prov="TV アニメーション「下級生」第5～7話　持田真歩子 テーマソング<br>収録「下級生 オリジナルサウンドトラック」",
         performer="ちざわゆうこ、轟太郎＆淡野保昌",
         staff="作詞：松本はるこ<br>作曲・編曲：轟太郎",
         zh=None),
    dict(no=20, slug="onethingiknow", src="elf-onethingiknow.txt",
         title="One thing I know",
         prov="「下級生」(1999)",
         performer="ちざわゆうこ、轟太郎＆淡野保昌",
         staff="作詞：松本はるこ<br>作曲・編曲：轟太郎",
         zh=None),
    # ===== Reflain Blue =====
    # --- らいむいろ戦記譚 ---
    dict(no=21, slug="rinka", src="elf-rinka.txt",
         title="凛花",
         prov="「らいむいろ戦記譚」オープニングテーマ (2003)",
         performer="らいむ隊",
         staff="",
         zh=None),
]

# 索引分组（每组合计数器重置，沿用 urusei / 橙路 风格）
# 外链条目：歌词页已删除，直接指向站内其他专区的对应页面
EXT_MIMI = 100   # 编号占位（不生成歌词页）
EXTLINKS = {
    EXT_MIMI: dict(title="耳をすませば", href="/galgame/refrainblue/ovasong.html", note="Reflain Blue ED"),
}

GROUPS = [
    ("专辑「élf ANIMATION SONG FILE」", "KSCA-59134 / 2000-07-21　全 15 首（收录顺序）", list(range(1, 15)) + [EXT_MIMI]),
    ("同級生２", "专辑未收录的单曲　4 首", [15, 16, 17, 18]),
    ("电视动画「下級生」", "专辑未收录的单曲　2 首", [19, 20]),
    ("らいむいろ戦記譚", "1 首", [21]),
]

# 未收录（歌词未入手）：只列条目、不生成歌词页
MISSING = [
    dict(title="羽のない天使", note="エルフ版 下級生 ED2", performer="茶山莉子"),
    dict(title="Motion", note="エルフ版 下級生 插曲", performer="安達まり"),
    dict(title="アイシテル…！", note="恋姫 2001年 続第1巻 ED", performer="Millio"),
    dict(title="Forever Precious Love", note="恋姫 2001年 続第2巻 ED", performer="Millio"),
]

# ---------------- 解析工具 ----------------
# 源库(lyric3.mdb)导出的 PUA 私用区字符 / 注音符号混入，统一订正
CHARFIX = {
    "\ue6c5": "\u54b2",   # 咲 (haru: 野に咲く)
    "\ue6c3": "\u8fbc",   # 込 (natsu/seamoonlight/voices)
    "\uead2": "\u546a",   # 呪 (natsu: 魔法の呪文)
    "\u3127": "\u30fc",   # 注音符号 ㄧ -> 长音符 ー (natsu: ウイザード/ずーっと)
    "\uff5e": "\u301c",
}
MOJIFIX = {
    # 方括号内为「汉字 + 振假名注音」，只取汉字、弃方括号与注音（CHARFIX 之后的形态）
    "[咲さ]": "咲",                               # haru：野に咲く
    "[込こ]": "込",                               # natsu：黙り込…
    "ハ一ト": "ハート",                            # suki：OCR 将长音符 ー 误作「一」
    "ミラ一ツェイド": "ミラーシェイド",              # onemoment：同上
    "默り込おと": "黙り込んで",                     # natsu：源转录残缺，据上下文还原
    "ENTERNAL": "ETERNAL",                       # VGMdb / stage1st 均作 ETERNAL
    "浅野保昌": "淡野保昌",                        # 编曲者 Yasumasa Awano
}

def read(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    for a, b in CHARFIX.items():
        s = s.replace(a, b)
    for a, b in MOJIFIX.items():
        s = s.replace(a, b)
    return s.replace("\r\n", "\n")

def body_of(t):
    lines = t.split("\n")
    seps = [i for i, l in enumerate(lines) if l.strip() and set(l.strip()) == {"="}]
    if len(seps) >= 2:
        return "\n".join(lines[seps[1] + 1:])
    return t

def split_stanzas(body):
    """源文件：逐行之间空一行；段落（stanza）之间空两行。
    按空行切分，空白块视为段落分隔符，非空块（单行）并入当前段落。"""
    stanzas, cur = [], []
    for block in body.split("\n\n"):
        line = block.strip()
        if line == "":
            if cur:
                stanzas.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        stanzas.append(cur)
    return stanzas

def is_mark(lines):
    return bool(lines) and lines[0] and lines[0][0] in MARKS

def fmt_para(lines):
    if not lines:
        return ""
    mark = is_mark(lines)
    out = []
    for i, l in enumerate(lines):
        if mark:
            out.append(l if i == 0 else IDEOSP + l.lstrip(IDEOSP + " "))
        else:
            out.append(l.lstrip(IDEOSP + " "))
    return "<p>" + "<br>\n".join(out) + "</p>"

def body_html(path):
    paras = split_stanzas(body_of(read(path)))
    return "\n".join(fmt_para(p) for p in paras)

def bilingual_twoblocks(jp_path, cn_path):
    jp = "\n".join(fmt_para(p) for p in split_stanzas(body_of(read(jp_path))))
    cn = "\n".join(fmt_para(p) for p in split_stanzas(body_of(read(cn_path))))
    sub = '<div style="color:#FFBBBB;font-size:13px;margin:18px 0 6px;">{h}</div>'
    return sub.format(h="日本語") + "\n" + jp + "\n" + sub.format(h="中文訳") + "\n" + cn

# ---------------- 模板 ----------------
PAGE_HEAD = '''<!DOCTYPE html> <!-- 声明文档类型为HTML5 -->
<html lang="ja"> <!-- HTML根元素 -->
<head>
    <meta charset="UTF-8"> <!-- 设置字符编码为UTF-8 -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- 响应式视口设置 -->
    <title>{title} - ELF</title> <!-- 页面标题 -->
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/lyric/lyric.css?v=11">
    <link rel="icon" href="/image/logo.webp" type="image">
</head>

<body>
    <script>
        // 加载页头
        fetch('/components/header.html')
            .then(response => response.text())
            .then(data => {{
                document.getElementById('header-container').innerHTML = data;
            }});

        // 加载页脚
        fetch('/components/footer.html')
            .then(response => response.text())
            .then(data => {{
                document.getElementById('footer-container').innerHTML = data;
            }});
    </script>

    <div class="container"> <!-- 主容器 -->
        <div id="header-container"></div> <!-- 页头加载 -->

        <main class="main-content"> <!-- 主内容区 -->
            <section class="main-section"> <!-- 主内容区块 -->
                <div class="LyricBody"> <!-- 歌词正文：整块居中，内部文字左对齐 -->
                    <div class="LyricProvenance">{prov}</div>

                    <div class="LyricTitle">{title}</div>
                    <hr class="LyricDivider">

                    <div class="LyricPerformer">{performer}</div>
                    <div class="LyricStaff">{staff}</div>

                    <div class="LyricText">
{body}                    </div>

                    <hr class="LyricFootRule">

                    <div class="LyricBack"><a href="{index}">← 曲目一覧</a></div>
                </div>
            </section>
        </main>

        <div id="footer-container"></div> <!-- 页脚通过JavaScript加载 -->
    </div>

</body>
</html>
'''

def lyric_page(s, body):
    return PAGE_HEAD.format(title=s["title"], prov=s["prov"], performer=s["performer"],
                           staff=s["staff"], body=body, index=INDEX)

def bilingual_page(s, body):
    title = s["title"] + "（日中対訳）"
    return PAGE_HEAD.format(title=title, prov=s["prov"], performer=s["performer"],
                           staff=s["staff"], body=body, index=INDEX)

# ---------------- 生成 ----------------
os.makedirs(DST, exist_ok=True)
os.makedirs(SRC, exist_ok=True)

_missing = [s["src"] for s in SONGS if not os.path.exists(os.path.join(SRC, s["src"]))]
if _missing:
    print(f"[warn] 源目录缺少歌词 txt，跳过歌词页生成：{SRC}")
    print("        缺失：", _missing)
else:
    # 重排编号后清理旧编号残留（编号会因重排变动，避免留下孤立文件）
    keep = {INDEX}
    for s in SONGS:
        keep.add(f'{s["no"]}.{s["slug"]}.html')
        if s["zh"]:
            keep.add(f'{s["no"]}.{s["slug"]}-bilingual.html')
    for f in sorted(glob.glob(os.path.join(DST, "*.html"))):
        b = os.path.basename(f)
        if b.startswith("0-"):
            continue
        if b not in keep:
            os.remove(f)
            print("removed stale:", b)
    for s in SONGS:
        b = body_html(os.path.join(SRC, s["src"]))
        with open(os.path.join(DST, f'{s["no"]}.{s["slug"]}.html'), "w", encoding="utf-8") as f:
            f.write(lyric_page(s, b))
        if s["zh"]:
            bb = bilingual_twoblocks(os.path.join(SRC, s["src"]), os.path.join(SRC, s["zh"]))
            with open(os.path.join(DST, f'{s["no"]}.{s["slug"]}-bilingual.html'), "w", encoding="utf-8") as f:
                f.write(bilingual_page(s, bb))
        print("built", s["no"], s["slug"], "zh=", bool(s["zh"]))

# ---------------- 索引页 ----------------
by_no = {s["no"]: s for s in SONGS}
group_html = []
NOTE = {
    # 专辑「élf ANIMATION SONG FILE」收录曲（带上所属作品，便于辨识）
    "everybrandnewday": "TVアニメ下級生 片头曲", "eternal": "ドラゴンナイト４ 片尾曲",
    "face": "YU-NO 第3・4幕 片尾曲", "color": "同級生２ TV編集版 片头曲",
    "suki": "エルフ版下級生 片尾曲", "girlsbeup": "TVアニメ下級生 片尾曲",
    "naze": "恋姫 片尾曲", "siawasenohana": "ビ・ヨンド 片尾曲",
    "rureto": "エルフ版下級生 特典", "seamoonlight": "エルフ版下級生 特典",
    "tokimeki": "エルフ版下級生 片头曲", "light": "同級生２ EXTRA BOX 特典",
    "suki2": "同級生２ Special 卒業生 片尾曲", "voices": "YU-NO 第1・2幕 片尾曲",
    # 专辑未收录的单曲
    "haru": "SS版 片尾曲", "natsu": "PCE版 主题曲",
    "onemoment": "同級生II", "sweetonyou": "同級生II",
    "summergirl": "第5～7话 插曲", "onethingiknow": "插曲", "rinka": "片头曲",
}
for gname, gsub, nums in GROUPS:
    items = []
    for n in nums:
        if n in EXTLINKS:                      # 外链条目（歌词页在别的专区）
            e = EXTLINKS[n]
            items.append(f'\t\t\t\t\t<li class="LyricItem"><a href="{e["href"]}">《{e["title"]}》</a><span class="note">- {e["note"]}</span></li>')
            continue
        s = by_no[n]
        zh_link = f'＆<a href="{s["no"]}.{s["slug"]}-bilingual.html">(中译)</a>' if s["zh"] else ""
        items.append(f'\t\t\t\t\t<li class="LyricItem"><a href="{s["no"]}.{s["slug"]}.html">《{s["title"]}》</a>{zh_link}<span class="note">- {NOTE[s["slug"]]}</span></li>')
    group_html.append(f'''                    <div class="disc-head"><span class="disc-name">{gname}</span><span class="disc-sub">{gsub}</span></div>
                    <ul class="song-list">
{chr(10).join(items)}
                    </ul>''')

INDEX_TPL = '''<!DOCTYPE html> <!-- 声明文档类型为HTML5 -->
<html lang="ja"> <!-- HTML根元素，设置语言为日文 -->
<head>
    <meta charset="UTF-8"> <!-- 设置字符编码为UTF-8 -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- 响应式视口设置 -->
    <title>Lyrics</title> <!-- 页面标题 -->
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="/lyric/lyric.css?v=11">
    <link rel="icon" href="/image/logo.webp" type="image">
    <style>
        /* 标题：图标与文字垂直居中 */
        .catalog-head {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .catalog-head img {{ width: 48px; height: 48px; }}
        .album-head {{ max-width: 760px; margin: 16px auto 4px; text-align: center; }}
        .album-title {{ font-family: 'MS Gothic', 'ＭＳ ゴシック', 'Yu Gothic', sans-serif; font-size: 18px; color: #E6D8AE; }}
        .album-meta {{ margin-top: 2px; font-size: 13px; color: #bbbbaa; }}
        .disc-head {{
            max-width: 760px; margin: 26px auto 0; padding-bottom: 6px;
            text-align: center; border-bottom: 1px solid #555540;
        }}
        .disc-name {{ font-family: 'MS Gothic', 'ＭＳ ゴシック', 'Yu Gothic', sans-serif; font-size: 17px; color: #CC66FF; margin-right: 10px; }}
        .disc-sub {{ font-size: 13px; color: #bbbbaa; }}
        .song-list {{
            list-style: none; padding: 0; margin: 8px auto 0; max-width: 760px;
            text-align: left; counter-reset: song;
        }}
        .song-list li {{ padding: 4px 10px; line-height: 1.9; }}
        .song-list li::before {{
            counter-increment: song;
            content: '✦ ' counter(song) ". ";
            color: #E6D8AE;
        }}
        .song-list a {{ font-family: 'MS Gothic', 'ＭＳ ゴシック', 'Yu Gothic', sans-serif; font-size: 17px; }}
        .song-list .note {{ margin-left: 8px; font-size: 14px; color: #bbbbaa; font-family: 'MS Gothic', 'ＭＳ ゴシック', 'Yu Gothic', sans-serif; }}
        .song-list-missing li {{ opacity: .7; }}
        .song-list-missing li::before {{ color: #8a8a7a; }}
        .LyricMemo {{ max-width: 760px; margin: 18px auto 0; font-size: 13px; color: #bbbbaa; line-height: 1.8; }}
    </style>
</head>

<body>
    <script>
        fetch('/components/header.html')
            .then(response => response.text())
            .then(data => {{ document.getElementById('header-container').innerHTML = data; }});
        fetch('/components/footer.html')
            .then(response => response.text())
            .then(data => {{ document.getElementById('footer-container').innerHTML = data; }});
    </script>

    <div class="container">
        <div id="header-container"></div>

        <main class="main-content">
            <section class="main-section">
                <div style="margin:20px;">
                    <div class="LyricCatalog catalog-head"><img src="../images/{img}"><span>ELF（エルフ）</span></div>
                    <hr style="margin:20px 0; border-top:1px solid #E6D8AE;">

                    <div class="album-head">
                        <div class="album-title">《ELF エルフ》</div>
                        <div class="album-meta">élf（エルフ）作品主题曲集　已收录 21 首（专辑 14 ＋ 单曲 7）／外链 1 首／未收录 4 首</div>
                    </div>

{groups}
                    <p class="LyricMemo">※ 排列：专辑「élf ANIMATION SONG FILE」全 15 首（收录顺序）→ 专辑未收录的单曲（按游戏分）→ 未收录。<br>※ 已收录 23 首（专辑 15 ＋ 单曲 8）；末组 4 首歌词未入手，仅列条目、未建页。<br>※ 源数据订正：「ENTERNAL」→「ETERNAL」、编曲者「浅野保昌」→「淡野保昌」；PUA 私用区字符已还原（咲／込／呪）。</p>

                    <hr style="margin:20px 0; border-top:1px solid #E6D8AE;">

                    <div class="LyricBack"><a href="../fullindex.html">← 曲目一覧</a></div>
                </div>
            </section>
        </main>

        <div id="footer-container"></div>
    </div>

</body>
</html>
'''

# 未収録组：只列条目、不给链接
if MISSING:
    items = []
    for m in MISSING:
        items.append('\t\t\t\t\t<li class="LyricItem LyricMissing">《%s》<span class="note">- %s／歌：%s　（未收录）</span></li>' % (m["title"], m["note"], m["performer"]))
    group_html.append(f'''                    <div class="disc-head"><span class="disc-name">未收录</span><span class="disc-sub">歌词未入手　{len(MISSING)} 首</span></div>
                    <ul class="song-list song-list-missing">
{chr(10).join(items)}
                    </ul>''')

with open(os.path.join(DST, INDEX), "w", encoding="utf-8") as f:
    f.write(INDEX_TPL.format(img=IMG, groups="\n".join(group_html)))
print("built index")

# ---------------- 归档 _map.py ----------------
ml = ["# -*- coding: utf-8 -*-", "# ELF（エルフ）歌词归档（纯数据，便于重建）", "SONGS = ["]
for s in SONGS:
    ml.append(f'    dict(no={s["no"]}, slug="{s["slug"]}", title="{s["title"]}", '
               f'prov="{s["prov"]}", performer="{s["performer"]}", '
               f'staff="{s["staff"].replace("<br>", " / ")}", zh={s["zh"]!r}),')
ml.append("]")
ml.append("")
ml.append("GROUPS = [")
for gname, gsub, nums in GROUPS:
    ml.append(f'    ({gname!r}, {gsub!r}, {nums}),')
ml.append("]")
with open(os.path.join(DST, "_map.py"), "w", encoding="utf-8") as f:
    f.write("\n".join(ml) + "\n")
print("built _map.py")

# ---------------- 校验：缩进规则违规检查 ----------------
def check_html_indent(path):
    """校验已生成的 HTML（缩进是在生成时写入的，须以成品为准）：
    标记段→首行顶格显示标记、第2行起缩进1全角空格；非标记段→全部顶格。"""
    with open(path, encoding="utf-8") as f:
        t = f.read()
    bad = []
    m = re.search(r'<div class="LyricText">\n(.*?)</div>', t, re.S)
    if not m:
        return [("no LyricText", os.path.basename(path))]
    # 注意：不可对行做 strip()——Python 的 strip() 会把 U+3000 全角空格一并剥掉，
    # 导致「已缩进」被误判为「未缩进」。此处只按 <br> 切分、仅用 .strip() 判空。
    for p in re.findall(r'<p>(.*?)</p>', m.group(1), re.S):
        lines = [l for l in p.split("<br>\n") if l.strip()]
        if not lines:
            continue
        if lines[0][0] in MARKS:
            if lines[0].startswith(IDEOSP):
                bad.append(("首行不应缩进", lines[0]))
            for l in lines[1:]:
                if not l.startswith(IDEOSP):
                    bad.append(("次行未缩进", l))
        else:
            for l in lines:
                if l.startswith(IDEOSP):
                    bad.append(("非标记段却缩进", l))
    return bad

print("--- 缩进规则校验（基于生成的 HTML）---")
if _missing:
    print("源文件缺失，跳过。")
else:
    total = 0
    for s in SONGS:
        for pagename in [f'{s["no"]}.{s["slug"]}.html'] + ([f'{s["no"]}.{s["slug"]}-bilingual.html'] if s["zh"] else []):
            b = check_html_indent(os.path.join(DST, pagename))
            total += len(b)
            print(f'{pagename:38s} 违规:', b if b else "0")
    print("合计违规:", total)
print("ALL DONE")
