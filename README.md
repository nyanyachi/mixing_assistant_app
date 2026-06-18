# Mixing Assistant

A Python-based web application that analyzes vocal recordings and provides mixing recommendations to help creators prepare tracks before the mixing process.

Built with Streamlit and audio analysis libraries, the application evaluates vocal characteristics such as loudness, dynamics, frequency balance, and sibilance, then generates practical mixing guidance.

## Live Demo

[https://...](https://mixingassistantapp.streamlit.app/)

## Overview

Mixing Assistant was created to help vocal cover creators quickly identify potential issues in their recordings before opening a DAW.

Rather than performing automatic mixing, the application analyzes audio features and provides recommendations for compression, de-essing, EQ adjustments, and workflow preparation.

The goal is to reduce guesswork and provide a structured starting point for vocal mixing.

## What This Project Demonstrates

* Python application development
* Audio feature extraction and analysis
* Interactive web application development with Streamlit
* Recommendation system design
* Multilingual user interface support
* CSV report generation
* User-focused workflow design
* Deployment and project maintenance workflows

## Features

### Audio Analysis

* WAV vocal file analysis
* Peak level analysis
* RMS loudness analysis
* Volume variation analysis
* Frequency band analysis

### Mixing Recommendations

* Compressor Need Score
* De-Esser Need Score
* EQ Assistant
* Mix Ready Indicator
* Fairlight Quick Start Workflow

### Additional Features

* CSV export
* Korean / English / Japanese support
* Multilingual user interface

## Language

- English (Current)
- [한국어](README_KR.md)
- [日本語](README_JP.md)

## Common Questions

- What should I adjust first?
- Do I need a Compressor?
- Do I need a De-Esser?
- Is the vocal too bright or too dark?



## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Tech Stack

- Python
- Streamlit
- Librosa
- NumPy
- Pandas
- SciPy

## Version

### v0.3

* Multilingual support added
* Korean / English / Japanese UI
* Improved Mix Coach workflow
* Improved Quick Start recommendations
* EQ Assistant localization
