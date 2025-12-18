# stress-check-23
本ツールは、厚生労働省が公表する「簡易版23項目ストレスチェック」（資料：[https://stresscheck.mhlw.go.jp/download/material/sc23.pdf](https://stresscheck.mhlw.go.jp/download/material/sc23.pdf)）を参考に作成したものです。

アプリURL：https://stress-check-23-zfdvky7at5epgn2jxsxbda.streamlit.app/#23

匿名で利用できます。各設問に回答すると、自動で合計点とストレスレベルを計算します。

※免責事項
本チェックは、あくまで「あなたの現在の心の傾向を知るため」のものであり、医師による診断や治療を目的としたものではありません。

心身の不調が続く、または強いストレスを感じる場合には、速やかに専門の医療機関や産業保健スタッフにご相談ください。

本ツールの利用によって生じたいかなる結果についても、作者は責任を負いかねます。


テスト方法
実行：pytest -q
採点ロジックはUIから分離し、自動テストで判定境界と異常入力を検証しています。
