# 🎙️ Mixing Assistant

Python と Streamlit で作成したボーカルミキシング補助アプリです。

Mixing Assistant は、カバー曲の録音後にミキシングを始める前の状態確認を目的として作られました。

このアプリは自動でミックスを完成させるものではありません。

代わりに次のような判断をサポートします。

* 最初に何を調整するべきか
* Compressor は必要か
* De-Esser は必要か
* ボーカルが明るすぎないか
* 低域が多すぎないか

## 主な機能

* WAV ボーカルファイル分析
* Peak 分析
* RMS 分析
* 音量変化分析
* 周波数帯分析
* Compressor 必要度表示
* De-Esser 必要度表示
* EQ Assistant
* Mix Ready 表示
* Fairlight 作業手順提案
* CSV 出力
* 韓国語 / 英語 / 日本語対応

## インストール

```bash
pip install -r requirements.txt
```

## 実行

```bash
streamlit run app.py
```

## 使用技術

* Python
* Streamlit
* Librosa
* NumPy
* Pandas
* SciPy

## バージョン

### v0.3

* 多言語対応追加
* 韓国語 / 英語 / 日本語 UI
* Mix Coach ワークフロー改善
* Quick Start 推奨改善
* EQ Assistant 多言語対応
