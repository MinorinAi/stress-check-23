import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# ===== 日本語フォント設定（matplotlib用） =====
# IPAexゴシックがStreamlit Cloudでも安定
plt.rcParams['font.family'] = 'IPAexGothic'

# ===== CIDフォント登録（PDF用） =====
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

# ===== Streamlit UI =====
st.title("ストレスチェック23項目（簡易版）")
st.write("匿名で利用できます。各設問に回答すると、自動で合計点とストレスレベルを計算します。")

# ===== 回答選択肢群 =====
options_1 = ["ほとんどなかった", "ときどきあった", "しばしばあった", "ほとんどいつもあった"]
options_2 = ["そうだ", "まあそうだ", "ややちがう", "ちがう"]
options_3 = ["非常に", "かなり", "多少", "全くない"]

# ===== 設問リスト =====
questions = [
    "ひどく疲れた","へとへとだ","だるい","気がはりつめている","不安だ","落ち着かない",
    "ゆううつだ","何をするのも面倒だ","気分が晴れない","食欲がない","よく眠れない",
    "非常にたくさんの仕事をしなければならない","時間内に仕事が処理しきれない","一生懸命働かなければならない",
    "自分のペースで仕事ができる","自分で仕事の順番・やり方を決めることができる","職場の仕事の方針に自分の意見を反映できる",
    "次の人たちはどれくらい気軽に話ができますか？【上司】","次の人たちはどれくらい気軽に話ができますか？【同僚】",
    "あなたが困った時、次の人たちはどれくらい頼りになりますか？【上司】","あなたが困った時、次の人たちはどれくらい頼りになりますか？【同僚】",
    "あなたの個人的な問題を相談したら、次の人たちはどれくらい聞いてくれますか？【上司】",
    "あなたの個人的な問題を相談したら、次の人たちはどれくらい聞いてくれますか？【同僚】"
]

# ===== 逆転項目 =====
reverse_items = [12, 13, 14]

# ===== 回答フォーム =====
st.markdown("### 【設問1〜11】最近1ヶ月のあなたの状態について")
answers = {}
for i in range(1, 12):
    ans = st.radio(f"{i}. {questions[i-1]}", options_1, index=0, horizontal=True)
    answers[i] = options_1.index(ans) + 1

st.markdown("### 【設問12〜17】あなたの仕事について")
for i in range(12, 18):
    ans = st.radio(f"{i}. {questions[i-1]}", options_2, index=0, horizontal=True)
    score = options_2.index(ans) + 1
    if i in reverse_items:
        score = 5 - score
    answers[i] = score

st.markdown("### 【設問18〜23】あなたの周りの方々について")
for i in range(18, 24):
    ans = st.radio(f"{i}. {questions[i-1]}", options_3, index=0, horizontal=True)
    answers[i] = options_3.index(ans) + 1

# ===== 合計算出 =====
A_total = sum([answers[i] for i in range(1, 12)])
B_total = sum([answers[i] for i in range(12, 24)])

# ===== 判定ロジック =====
if B_total <= 38:
    if A_total <= 15:
        level = "Ⅰ"
    elif A_total <= 22:
        level = "Ⅱ"
    elif A_total <= 30:
        level = "Ⅱ"
    else:
        level = "Ⅲ"
else:
    if A_total <= 15:
        level = "Ⅱ"
    elif A_total <= 22:
        level = "Ⅱ"
    elif A_total <= 30:
        level = "Ⅲ"
    else:
        level = "Ⅲ"

comment = {
    "Ⅰ": "ストレスは軽度です。仕事や生活への影響は少ない状態です。",
    "Ⅱ": "中程度のストレスがあります。疲労がありつつも仕事を続けられています。",
    "Ⅲ": "高ストレス状態です。健康や業務に支障をきたす恐れがあります。"
}[level]

# ===== グラフ作成 =====
plt.figure(figsize=(4,3))
plt.bar(["A（1〜11）", "B（12〜23）"], [A_total, B_total],
        color=["#66b3ff", "#99cc99"], edgecolor="black")
plt.title(f"ストレスチェック結果（レベル {level}）")
plt.ylabel("合計スコア")
plt.ylim(0, 50)
plt.tight_layout()
plt.savefig("stress_chart.png", dpi=150)
plt.close()

st.image("stress_chart.png", caption="スコア比較グラフ")

st.write(f"**A合計点（1〜11）:** {A_total}")
st.write(f"**B合計点（12〜23）:** {B_total}")
st.write(f"**ストレスレベル:** {level}")
st.info(comment)

# ===== PDF生成 =====
def generate_pdf(A_total, B_total, level, comment):
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle("Title", parent=styles["Heading1"], fontName='HeiseiKakuGo-W5',
                                 alignment=1, fontSize=18, textColor=colors.darkblue)
    style_normal = ParagraphStyle("Normal", parent=styles["Normal"], fontName='HeiseiMin-W3',
                                  fontSize=11, leading=14)
    style_sub = ParagraphStyle("Sub", parent=styles["Normal"], fontName='HeiseiKakuGo-W5',
                               fontSize=12, textColor=colors.grey)

    report_id = str(uuid.uuid4())[:8]
    date_str = datetime.now().strftime("%Y年%m月%d日")
    doc = SimpleDocTemplate("stress23_report.pdf", pagesize=A4)

    elements = [
        Paragraph("ストレスチェック23項目 結果レポート", style_title),
        Paragraph(date_str, style_sub),
        Spacer(1, 12),
        Paragraph(f"レポートID: {report_id}", style_normal),
        Paragraph(f"A合計点（1〜11）: {A_total}", style_normal),
        Paragraph(f"B合計点（12〜23）: {B_total}", style_normal),
        Paragraph(f"ストレスレベル: {level}", style_normal),
        Spacer(1, 12),
        Paragraph("【コメント】", style_sub),
        Paragraph(comment, style_normal),
        Spacer(1, 24),
        Image("stress_chart.png", width=300, height=200)
    ]
    doc.build(elements)
    return "stress23_report.pdf"

if st.button("PDFレポートを生成"):
    pdf_path = generate_pdf(A_total, B_total, level, comment)
    with open(pdf_path, "rb") as f:
        st.download_button("PDFをダウンロード", f, file_name="stress23_report.pdf")
