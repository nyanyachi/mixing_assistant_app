# 🎙️ Mixing Assistant

A small vocal mixing assistant built with Python and Streamlit.

Mixing Assistant is designed to help vocal cover creators analyze recordings before starting the mixing process.

This is not an automatic mixing tool.

## Language

- English (Current)
- [한국어](README_KR.md)
- [日本語](README_JP.md)

Instead, it helps answer:

* What should I adjust first?
* Do I need a Compressor?
* Do I need a De-Esser?
* Is the vocal too bright or too dark?

## Features

* WAV vocal file analysis
* Peak level analysis
* RMS loudness analysis
* Volume variation analysis
* Frequency band analysis
* Compressor Need score
* De-Esser Need score
* EQ Assistant
* Mix Ready indicator
* Fairlight Quick Start workflow
* CSV export
* Korean / English / Japanese support

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Technology

* Python
* Streamlit
* Librosa
* NumPy
* Pandas
* SciPy

## Version

### v0.3

* Multilingual support added
* Korean / English / Japanese UI
* Improved Mix Coach workflow
* Improved Quick Start recommendations
* EQ Assistant localization
