import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
from datetime import datetime
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# ===== CIDフォント登録（日本語対応） =====
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))   # 明朝体
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))  # ゴシック体

# ===== Streamlit UI =====
st.title("ストレスチェック23項目（簡易版）")
st.write("匿名で利用できます。各項目の合計点を入力すると、PDFレポートを自動生成します。")

# ===== 入力欄 =====
A_total = st.number_input("A合計（設問1〜11）", min_value=0, max_value=44, value=20)
B_total = st.number_input("B合計（設問12〜23）", min_value=0, max_value=48, value=30)

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

if level == "Ⅰ":
    comment = "ストレスは軽度です。仕事や生活への影響は少ない状態です。"
elif level == "Ⅱ":
    comment = "中程度のストレスがあります。疲労がありつつも仕事を続けられています。"
else:
    comment = "高ストレス状態です。健康や業務に支障をきたす恐れがあります。"

# ===== グラフ作成 =====
plt.figure(figsize=(4,3))
plt.bar(["A（1〜11）", "B（12〜23）"], [A_total, B_total],
        color=["#66b3ff", "#99cc99"], edgecolor="black")
plt.title(f"ストレスチェック結果（レベル {level}）", fontname="IPAexGothic")
plt.ylabel("合計スコア", fontname="IPAexGothic")
plt.ylim(0, 50)
plt.tight_layout()
plt.savefig("stress_chart.png", dpi=150)
plt.close()

st.image("stress_chart.png", caption="スコア比較グラフ", use_container_width=False)

# ===== PDF生成関数 =====
def generate_pdf(A_total, B_total, level, comment):
    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName='HeiseiKakuGo-W5',
        alignment=1,
        fontSize=18,
        textColor=colors.darkblue
    )

    style_normal = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontName='HeiseiMin-W3',
        fontSize=11,
        leading=14
    )

    style_sub = ParagraphStyle(
        "Sub",
        parent=styles["Normal"],
        fontName='HeiseiKakuGo-W5',
        fontSize=12,
        textColor=colors.grey
    )

    report_id = str(uuid.uuid4())[:8]
    date_str = datetime.now().strftime("%Y年%m月%d日")
    doc = SimpleDocTemplate("stress23_report.pdf", pagesize=A4)

    elements = []
    elements.append(Paragraph("ストレスチェック23項目 結果レポート", style_title))
    elements.append(Paragraph(date_str, style_sub))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"レポートID: {report_id}", style_normal))
    elements.append(Paragraph(f"A合計点（1〜11）: {A_total}", style_normal))
    elements.append(Paragraph(f"B合計点（12〜23）: {B_total}", style_normal))
    elements.append(Paragraph(f"ストレスレベル: {level}", style_normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("【コメント】", style_sub))
    elements.append(Paragraph(comment, style_normal))
    elements.append(Spacer(1, 24))

    elements.append(Image("stress_chart.png", width=300, height=200))

    doc.build(elements)
    return "stress23_report.pdf"

# ===== ボタン処理 =====
if st.button("PDFレポートを生成"):
    pdf_path = generate_pdf(A_total, B_total, level, comment)
    with open(pdf_path, "rb") as f:
        st.download_button("PDFをダウンロード", f, file_name="stress23_report.pdf")
