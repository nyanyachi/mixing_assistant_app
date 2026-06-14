import numpy as np
import librosa


def amp_to_db(value):
    value = max(value, 1e-10)
    return 20 * np.log10(value)


def analyze_audio(file, T):
    y, sr = librosa.load(file, sr=None, mono=True)

    duration = librosa.get_duration(y=y, sr=sr)

    peak_amp = np.max(np.abs(y))
    peak_db = amp_to_db(peak_amp)

    rms = librosa.feature.rms(y=y)[0]
    rms_mean = np.mean(rms)
    rms_db = amp_to_db(rms_mean)

    volume_variation = np.std(rms)
    volume_variation_db = amp_to_db(volume_variation)

    result = {
        "sample_rate": sr,
        "duration_sec": duration,
        "peak_db": peak_db,
        "rms_db": rms_db,
        "volume_variation_db": volume_variation_db,
    }

    # 추가 1.5V
    freq_info = analyze_frequency_bands(y, sr)
    result.update(freq_info)

    # 추가 1.6V
    result["compressor_score"] = calculate_compressor_score(result)
    preset = compressor_preset(result["compressor_score"])
    result["compressor_ratio"] = preset["ratio"]
    result["compressor_threshold"] = preset["threshold"]
    result["compressor_attack"] = preset["attack"]
    result["compressor_release"] = preset["release"]
    result["compressor_makeup_gain"] = preset["makeup_gain"]
    # 추가 2.5V
    result["sibilance_percent"] = (analyze_sibilance(y, sr))
    result["deesser_score"] = (calculate_deesser_score(result["sibilance_percent"]))
    # 추가 3.0V
    result["mix_score"] = (calculate_mix_score(result))
    # 추가 3.5V
    result["quick_start"] = (generate_quick_start(result,T))
    # 추가 4.0V
    result["eq_suggestions"] = (generate_eq_suggestions(result,T))
    # 추가 4.5V
    result["mix_comment"] = (generate_mix_comment(result, T))

    return result

# 추가 1.5V
def analyze_frequency_bands(y, sr):

    stft = np.abs(librosa.stft(y))

    freqs = librosa.fft_frequencies(sr=sr)

    total_energy = np.sum(stft)

    low_mask = (freqs >= 20) & (freqs < 250)
    mid_mask = (freqs >= 250) & (freqs < 4000)
    high_mask = (freqs >= 4000) & (freqs < 12000)

    low_energy = np.sum(stft[low_mask])
    mid_energy = np.sum(stft[mid_mask])
    high_energy = np.sum(stft[high_mask])

    return {
        "low_percent": low_energy / total_energy * 100,
        "mid_percent": mid_energy / total_energy * 100,
        "high_percent": high_energy / total_energy * 100
    }

def calculate_compressor_score(result):

    score = 0

    peak_db = result["peak_db"]
    rms_db = result["rms_db"]
    variation_db = result["volume_variation_db"]

    # Peak와 RMS 차이
    dynamic_range = peak_db - rms_db

    # 다이나믹이 클수록 압축 필요
    if dynamic_range > 20:
        score += 40
    elif dynamic_range > 15:
        score += 30
    elif dynamic_range > 10:
        score += 20

    # 볼륨 편차
    if variation_db > -20:
        score += 40
    elif variation_db > -25:
        score += 30
    elif variation_db > -30:
        score += 20

    # RMS가 너무 낮으면 약간 가산
    if rms_db < -25:
        score += 10

    score = min(score, 100)

    return score

# 추가 1.6V
def compressor_preset(score):
    if score >= 70:
        return {
            "ratio": "4:1",
            "threshold": "-20 dB",
            "attack": "10 ms",
            "release": "100 ms",
            "makeup_gain": "+2 dB"
        }

    elif score >= 40:
        return {
            "ratio": "3:1",
            "threshold": "-18 dB",
            "attack": "15 ms",
            "release": "120 ms",
            "makeup_gain": "+1 dB"
        }

    else:
        return {
            "ratio": "2:1",
            "threshold": "-15 dB",
            "attack": "20 ms",
            "release": "150 ms",
            "makeup_gain": "0 dB"
        }
    
# 추가 2.5V
def analyze_sibilance(y, sr):

    stft = np.abs(librosa.stft(y))

    freqs = librosa.fft_frequencies(sr=sr)

    total_energy = np.sum(stft)

    sibilance_mask = (
        (freqs >= 5000) &
        (freqs <= 9000)
    )

    sibilance_energy = np.sum(
        stft[sibilance_mask]
    )

    percent = (
        sibilance_energy /
        total_energy
    ) * 100

    return percent

def calculate_deesser_score(
    sibilance_percent
):

    if sibilance_percent > 12:
        return 90

    elif sibilance_percent > 8:
        return 70

    elif sibilance_percent > 5:
        return 50

    else:
        return 20
    
# 추가 3.0V
def calculate_mix_score(
    result
):

    score = 100

    if result["peak_db"] > -1:
        score -= 10

    if result["compressor_score"] > 80:
        score -= 10

    if result["deesser_score"] > 80:
        score -= 10

    if result["low_percent"] > 30:
        score -= 10

    return max(score, 0)

# 추가 3.5V
def generate_quick_start(result, T):
    steps = []

    if result["peak_db"] > -3:
        steps.append(T["quick_clip_gain_down"])
    else:
        steps.append(T["quick_clip_gain_ok"])

    if result["low_percent"] > 25:
        steps.append(T["quick_eq_lowcut"])
    elif result["high_percent"] > 15:
        steps.append(T["quick_eq_high"])
    elif result["high_percent"] < 6:
        steps.append(T["quick_eq_air"])
    else:
        steps.append(T["quick_eq_ok"])

    if result["compressor_score"] >= 70:
        steps.append(
            T["quick_comp_strong"].format(
                ratio=result["compressor_ratio"],
                threshold=result["compressor_threshold"]
            )
        )
    elif result["compressor_score"] >= 40:
        steps.append(
            T["quick_comp_normal"].format(
                ratio=result["compressor_ratio"],
                threshold=result["compressor_threshold"]
            )
        )
    else:
        steps.append(T["quick_comp_low"])

    if result["deesser_score"] >= 70:
        steps.append(T["quick_deesser_strong"])
    elif result["deesser_score"] >= 40:
        steps.append(T["quick_deesser_normal"])
    else:
        steps.append(T["quick_deesser_low"])

    steps.append(T["quick_reverb"])

    return steps[:3]

# 추가 4.0V
def generate_eq_suggestions(result, T):

    suggestions = []

    low = result["low_percent"]
    high = result["high_percent"]

    if low > 25:
        suggestions.append(
            T["eq_lowcut"]
        )

    if low > 30:
        suggestions.append(
            T["eq_low_cut_150"]
        )

    if high < 6:
        suggestions.append(
            T["eq_air_boost"]
        )

    if high > 15:
        suggestions.append(
            T["eq_high_check"]
        )

    if not suggestions:
        suggestions.append(
            T["eq_not_needed"]
        )

    return suggestions

# 추가 4.5V
def generate_mix_comment(result, T):
    comment = []

    if result["high_percent"] > 15:
        comment.append(T["comment_bright"])

    elif result["low_percent"] > 25:
        comment.append(T["comment_warm"])

    else:
        comment.append(T["comment_balanced"])

    if result["deesser_score"] >= 70:
        comment.append(T["comment_sibilance"])

    if result["compressor_score"] >= 60:
        comment.append(T["comment_compressor"])

    return comment