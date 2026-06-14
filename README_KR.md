# 🎙️ Mixing Assistant

Python과 Streamlit으로 제작한 보컬 믹싱 보조 앱입니다.

Mixing Assistant는 커버곡 녹음 후 믹싱을 시작하기 전에 보컬 상태를 빠르게 확인할 수 있도록 만들어졌습니다.

이 앱은 자동으로 믹싱을 해주는 도구가 아닙니다.

대신 다음과 같은 질문에 도움을 줍니다.

* 무엇을 먼저 만져야 할까?
* Compressor가 필요할까?
* De-Esser가 필요할까?
* 보컬이 너무 밝을까?
* 저역이 너무 많을까?

## 주요 기능

* WAV 보컬 파일 분석
* Peak 분석
* RMS 분석
* 볼륨 편차 분석
* 주파수 대역 분석
* Compressor 필요도 표시
* De-Esser 필요도 표시
* EQ Assistant
* Mix Ready 표시
* Fairlight 작업 순서 추천
* CSV 저장
* 한국어 / 영어 / 일본어 지원

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
streamlit run app.py
```

## 사용 기술

* Python
* Streamlit
* Librosa
* NumPy
* Pandas
* SciPy

## 버전

### v0.3

* 다국어 지원 추가
* 한국어 / 영어 / 일본어 UI 지원
* Mix Coach 워크플로우 개선
* Quick Start 추천 개선
* EQ Assistant 다국어 지원
