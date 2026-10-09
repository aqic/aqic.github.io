# -*- coding: utf-8 -*-
import os

# 基于脚本自身位置定位，便于在本目录内独立复用：
#   BASE = 本脚本所在目录 (shenmue)
#   DST  = 输出 HTML / 索引 / _map.py 到本目录
#   SRC  = 源歌词 txt 放在本目录下的 src/ 子目录（与脚本同级）
BASE = os.path.dirname(os.path.abspath(__file__))
DST = BASE
SRC = os.path.join(BASE, "src")
IMG = "shenmue.gif"
INDEX = "0-shenmue-index.html"

MARKS = "※★☆◇◆＊"
IDEOSP = "\u3000"

# ---- 歌曲元数据（已对照网上资料订正出处/制作）----
SONGS = [
    dict(no=1, slug="shenhua", src="shenmu-shenhua.txt",
         title="莎花～江清日抱花歌～",
         prov="DCゲーム「シェンムー 一章 横須賀」挿入歌／イメージソング(1999)",
         performer="伊織",
         staff="作詞：浅田由美<br>作曲：井内竜次<br>編曲：松尾早人",
         zh="shenmu-shenhua_中.txt"),
    dict(no=2, slug="wish", src="shenmu-wish.txt",
         title="Wish...",
         prov="「シェンムー 一章 横須賀」オリジナルサウンドトラック(2000)　Disc2 収録",
         performer="山本由美子(Yumiko Yamamoto)",
         staff="作詞：Yumi Asada(浅田由美)<br>作曲：Ryuji Iuchi(井内竜次)",
         zh=None),
]

# 索引分组（每组合计数器重置，沿用 urusei / 橙路 风格）
GROUPS = [
    ("主题曲・插曲", "「莎木」相关　2 首", [1, 2]),
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
    <title>{title} - 莎木</title> <!-- 页面标题 -->
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
NOTE = {"shenhua": "插曲／印象歌(1999)", "wish": "原声收录(2000)"}
for gname, gsub, nums in GROUPS:
    items = []
    for n in nums:
        s = by_no[n]
        zh_link = f'＆<a href="{s["no"]}.{s["slug"]}-bilingual.html">(中译)</a>' if s["zh"] else ""
        items.append(f'\t\t\t\t\t<li class="LyricItem"><a href="{s["no"]}.{s["slug"]}.html">《{s["title"]}》</a>{zh_link}<span class="note">- {NOTE[s["slug"]]}</span></li>')
    group_html.append(f'''                    <div class="disc-head"><span class="disc-name">{gname}</span><span class="disc-sub">{gsub}</span></div>
                    <ul class="song-list">
{chr(10).join(items)}
                    </ul>''')

# 未收录曲目：灰显不可点（沿用 urusei 既有原则）
MISSING = [
    ("You're my only…… ～シェンムーのささやき～", "主题曲(1999)／歌：Kuming"),
]
_missing_items = [
    f'\t\t\t\t\t<li class="LyricItem LyricMissing"><span class="mtitle">《{t}》</span><span class="note">- {note}（未收录）</span></li>'
    for t, note in MISSING
]
group_html.append(f'''                    <div class="disc-head"><span class="disc-name">未收录</span><span class="disc-sub">歌词未入手{len(MISSING)} 首</span></div>
                    <ul class="song-list">
{chr(10).join(_missing_items)}
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
    <link rel="stylesheet" href="/lyric/index.css?v=1">
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
                    <div class="LyricCatalog catalog-head"><img src="../images/{img}"><span>莎木（シェンムー / Shenmue）</span></div>
                    <hr style="margin:20px 0; border-top:1px solid #E6D8AE;">

                    <div class="album-head">
                        <div class="album-title">《莎木》</div>
                        <div class="album-meta">セガ Dreamcast ゲーム「シェンムー 一章 横須賀」関連　已收录 2 首</div>
                    </div>

{groups}
                    <p class="LyricMemo">※ 本辑收录 2 首已整理歌词，另列 1 首暂无歌词的曲目。</p>

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
