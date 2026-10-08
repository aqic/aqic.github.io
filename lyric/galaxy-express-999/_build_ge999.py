# -*- coding: utf-8 -*-
import os

# 基于脚本自身位置定位，便于在本目录内独立复用：
#   BASE = 本脚本所在目录 (galaxy-express-999)
#   DST  = 输出 HTML / 索引 / _map.py 到本目录
#   SRC  = 源歌词 txt 放在本目录下的 src/ 子目录（与脚本同级）
BASE = os.path.dirname(os.path.abspath(__file__))
DST = BASE
SRC = os.path.join(BASE, "src")
IMG = "galaxy-express-999.gif"
INDEX = "0-galaxy-express-999-index.html"

MARKS = "※★☆◇◆＊"
IDEOSP = "\u3000"

# ---- 歌曲元数据（已对照网上资料订正出处/制作）----
SONGS = [
    dict(no=1, slug="galaxyexpress999", src="ge999-galaxyexpress999.txt",
         title="銀河鉄道999",
         prov="テレビアニメ「銀河鉄道999」オープニング(1978)",
         performer="ささきいさお(佐々木 功)、杉並兒童合唱團",
         staff="作詞：橋本淳<br>作曲：平尾昌晃<br>編曲：青木望",
         zh="ge999-galaxyexpress999_中.txt"),
    dict(no=2, slug="blueearth", src="ge999-blueearth.txt",
         title="青い地球",
         prov="テレビアニメ「銀河鉄道999」エンディング(1978)",
         performer="ささきいさお(佐々木 功)、杉並兒童合唱團",
         staff="作詞：橋本淳<br>作曲：平尾昌晃<br>編曲：青木望",
         zh="ge999-blueearth_中.txt"),
    dict(no=3, slug="takingoff", src="ge999-takingoff.txt",
         title="TAKING OFF!",
         prov="劇場版1「銀河鉄道999」挿入歌(1979)",
         performer="ゴダイゴ",
         staff="作詞：奈良橋陽子、山川啟介<br>作曲：タケカワユキヒデ",
         zh=None),
    dict(no=4, slug="thege999", src="ge999-thege999.txt",
         title="THE GALAXY EXPRESS",
         prov="劇場版1「銀河鉄道999」エンディング(1979)",
         performer="ゴダイゴ",
         staff="作詞：奈良橋陽子、山川啟介<br>作曲：タケカワユキヒデ",
         zh=None),
    dict(no=5, slug="yasaxii", src="ge999-yasaxii.txt",
         title="やさしくしないで",
         prov="劇場版1「銀河鉄道999」挿入歌(1979)",
         performer="かおりくみこ",
         staff="作詞：中原葉子<br>作曲：中村泰<br>編曲：青木望",
         zh="ge999-yasaxii_中.txt"),
    dict(no=6, slug="sayonara", src="ge999-sayonara.txt",
         title="SAYONARA",
         prov="劇場版2「さよなら銀河鉄道999」エンディング(1981)",
         performer="Mary Macgregor",
         staff="作詞：Mary Macgregor<br>作曲：Brian Whitcomb & Mary Macgregor",
         zh=None),
    dict(no=7, slug="bravelove", src="ge999-bravelove.txt",
         title="Brave Love～",
         prov="劇場版3「エターナル・ファンタジー」主題歌(1998)",
         performer="THE ALFEE",
         staff="作詞・作曲：高見沢俊彦<br>編曲：THE ALFEE",
         zh=None),
]

# 索引分组（每组合计数器重置，沿用 urusei / 橙路 风格）
GROUPS = [
    ("TVアニメ", "テレビシリーズ(1978–1981)　主題歌 2 首", [1, 2]),
    ("劇場版1「銀河鉄道999」", "1979年公開　主題関連 3 首", [3, 4, 5]),
    ("劇場版2「さよなら銀河鉄道999」", "1981年公開　1 首", [6]),
    ("劇場版3「エターナル・ファンタジー」", "1998年公開　1 首", [7]),
]

# ---------------- 解析工具 ----------------
def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

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
    <title>{title} - 銀河鉄道999</title> <!-- 页面标题 -->
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
NOTE = {"galaxyexpress999": "オープニング(1978)", "blueearth": "エンディング(1978)",
        "takingoff": "挿入歌(1979)", "thege999": "エンディング(1979)",
        "yasaxii": "挿入歌(1979)", "sayonara": "エンディング(1981)",
        "bravelove": "主題歌(1998)"}
for gname, gsub, nums in GROUPS:
    items = []
    for n in nums:
        s = by_no[n]
        zh_link = f'-<a href="{s["no"]}.{s["slug"]}-bilingual.html">（中译）</a>' if s["zh"] else ""
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
        .song-list .note {{ margin-left: 8px; font-size: 14px; color: #bbbbaa; }}
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
                    <div class="LyricCatalog catalog-head"><img src="../images/{img}"><span>銀河鉄道999（ギャラクシー・エクスプレス999）</span></div>
                    <hr style="margin:20px 0; border-top:1px solid #E6D8AE;">

                    <div class="album-head">
                        <div class="album-title">《銀河鉄道999》</div>
                        <div class="album-meta">松本零士原作　テレビアニメ(1978–1981) ＋ 劇場版3作　已收录 7 首代表曲</div>
                    </div>

{groups}
                    <p class="LyricMemo">※ 本辑仅收录 OP/ED 与剧场版主题・插入歌等 7 首代表曲。TV 插入歌集（『銀河鉄道999 主題歌・挿入歌集』CS-7096）及剧场版其他插入歌（如「想い出涙色」「LOVE LIGHT」「さよなら」等）另有未收录曲目。</p>

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

with open(os.path.join(DST, INDEX), "w", encoding="utf-8") as f:
    f.write(INDEX_TPL.format(img=IMG, groups="\n".join(group_html)))
print("built index")

# ---------------- 归档 _map.py ----------------
ml = ["# -*- coding: utf-8 -*-", "# 银河铁道999 歌词归档（纯数据，便于重建）", "SONGS = ["]
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
def check_indent(path):
    bad = []
    paras = split_stanzas(body_of(read(path)))
    for p in paras:
        if is_mark(p):
            for i, l in enumerate(p):
                if i == 0:
                    if l[0] not in MARKS:
                        bad.append(("首行缺标记", l))
                else:
                    if not l.startswith(IDEOSP):
                        bad.append(("次行未缩进", l))
        else:
            for l in p:
                if l.startswith(IDEOSP):
                    bad.append(("非标记段却缩进", l))
    return bad

print("--- 缩进规则校验 ---")
if _missing:
    print("源文件缺失，跳过缩进校验。")
else:
    for s in SONGS:
        b = check_indent(os.path.join(SRC, s["src"]))
        print(s["slug"], "违规:", b if b else "0")
print("ALL DONE")
