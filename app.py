import streamlit as st
import pandas as pd
from languages.Ko import TEXT as KO
from languages.En import TEXT as EN
from languages.Jp import TEXT as JP
from audio_analyzer import analyze_audio


st.set_page_config(
    page_title="Mixing Assistant",
    page_icon="🎙️",
    layout="wide"
)


def get_need_label(score):

    if score < 30:
        return "🟢 필요 낮음"

    elif score < 70:
        return "🟡 사용 권장"

    else:
        return "🔴 적극 권장"


def get_mix_label(score):

    if score < 50:
        return "🔴 작업 전 확인 필요"

    elif score < 80:
        return "🟡 작업 가능"

    else:
        return "🟢 작업 시작 가능"

language = st.sidebar.selectbox(
    "Language",
    ["한국어", "English", "日本語"]
)

if language == "한국어":
    T = KO

elif language == "English":
    T = EN

else:
    T = JP


st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0E1117 !important;
    color: #FFFFFF !important;
}

[data-testid="stHeader"] {
    background-color: #0E1117 !important;
}

[data-testid="stToolbar"] {
    background-color: #0E1117 !important;
}

.main {
    background-color: #0E1117 !important;
}

[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

st.title(T["title"])
st.write(T["description"])

with st.sidebar:
    st.header(T["sidebar"])
    uploaded_file = st.file_uploader(T["upload"], type=["wav"])

    if uploaded_file is not None:
        with st.expander(T["preview"], expanded=True):
            st.audio(uploaded_file)

if uploaded_file is not None:
    with st.spinner(T["analyzing"]):
        uploaded_file.seek(0)
        result = analyze_audio(uploaded_file, T)

    st.header(T["mix_comment"])

    for item in result["mix_comment"]:
        st.info(item)

    st.divider()

    st.header(T["quick_start"])

    for item in result["quick_start"]:
        st.info(item)

    st.divider()

    st.subheader(T["core_scores"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            T["mix_ready"],
            f"{result['mix_score']}/100"
        )

        st.caption(
            get_mix_label(result["mix_score"])
        )

        st.progress(
            result["mix_score"] / 100
        )

    with col2:
        st.metric(
            T["compressor_need"],
            f"{result['compressor_score']}/100"
        )

        st.caption(
            get_need_label(
                result["compressor_score"]
            )
        )

        st.progress(
            result["compressor_score"] / 100
        )

    with col3:
        st.metric(
            T["deesser_need"],
            f"{result['deesser_score']}/100"
        )

        st.caption(
            get_need_label(
                result["deesser_score"]
            )
        )

        st.progress(
            result["deesser_score"] / 100
        )

    if result["mix_score"] >= 90:
        st.success(
            T["mix_ready_message"]
        )

    elif result["mix_score"] >= 70:
        st.warning(
            T["warning_message"]
        )

    else:
        st.error(
            T["error_message"]
        )

    st.divider()

    st.subheader(T["details"])

    with st.expander(T["preview_results"]):
        col1, col2 = st.columns(2)

        with col1:
            st.metric(T["duration"], f"{result['duration_sec']:.2f} sec")
            st.metric(T["sample_rate"], f"{result['sample_rate']} Hz")
            st.metric(T["volume_variation"], f"{result['volume_variation_db']:.2f} dB")

        with col2:
            st.metric(T["peak"], f"{result['peak_db']:.2f} dB")
            st.metric(T["rms"], f"{result['rms_db']:.2f} dB")

    with st.expander(T["frequency_analysis"]):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(T["low_frequency"], f"{result['low_percent']:.1f}%")

        with col2:
            st.metric(T["mid_frequency"], f"{result['mid_percent']:.1f}%")

        with col3:
            st.metric(T["high_frequency"], f"{result['high_percent']:.1f}%")

        with col4:
            st.metric(T["sibilance_frequency"], f"{result['sibilance_percent']:.1f}%")

    with st.expander(T["compressor_recommendations"]):
        st.metric(T["compressor_need"], f"{result['compressor_score']}/100")
        st.write(f"Ratio: **{result['compressor_ratio']}**")
        st.write(f"Threshold: **{result['compressor_threshold']}**")
        st.write(f"Attack: **{result['compressor_attack']}**")
        st.write(f"Release: **{result['compressor_release']}**")
        st.write(f"Makeup Gain: **{result['compressor_makeup_gain']}**")

    with st.expander(T["deesser_analysis"]):
        st.metric(T["deesser_need"], f"{result['deesser_score']}/100")
        st.write(f"{T['sibilance_frequency']}: **{result['sibilance_percent']:.1f}%**")
        st.write(f"{T['deesser_note']}")

    with st.expander(T["eq_assistant"]):
        for item in result["eq_suggestions"]:
            st.write(f"• {item}")

    with st.expander(T["csv"]):
        df = pd.DataFrame([{
            "duration_sec": result["duration_sec"],
            "sample_rate": result["sample_rate"],
            "peak_db": result["peak_db"],
            "rms_db": result["rms_db"],
            "volume_variation_db": result["volume_variation_db"],
            "low_percent": result["low_percent"],
            "mid_percent": result["mid_percent"],
            "high_percent": result["high_percent"],
            "sibilance_percent": result["sibilance_percent"],
            "compressor_score": result["compressor_score"],
            "compressor_ratio": result["compressor_ratio"],
            "compressor_threshold": result["compressor_threshold"],
            "deesser_score": result["deesser_score"],
            "mix_score": result["mix_score"],
            "quick_start": " / ".join(result["quick_start"])
        }])

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label=T["download"],
            data=csv,
            file_name="mixing_analysis.csv",
            mime="text/csv"
        )

else:
    st.info(T["waiting"])
