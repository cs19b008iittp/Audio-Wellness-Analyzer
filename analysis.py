import whisper
import librosa
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import uuid

model = whisper.load_model("base")

# Dummy baseline samples (in real app, use real training data)
baseline_samples = np.array([
    [5, 1, 2.5, 80, 0.015, 0.08],  # normal
    [8, 2, 1.8, 120, 0.02, 0.1],  # normal
    [12, 5, 1.0, 200, 0.03, 0.2],  # potential risk
])

def analyze_audio(file_path):
    # Step 1: Transcribe
    result = model.transcribe(file_path)
    transcript = result["text"]

    # Step 2: Load audio
    y, sr = librosa.load(file_path)
    duration = librosa.get_duration(y=y, sr=sr)

    # Step 3: Feature Extraction
    pauses = transcript.count(".") + transcript.count(",")
    hesitations = sum(transcript.lower().count(h) for h in ["uh", "um"])
    speech_rate = len(transcript.split()) / duration

    pitch = librosa.yin(y, fmin=75, fmax=500)
    pitch_var = np.var(pitch)
    pitch_mean = np.mean(pitch)

    energy = np.mean(librosa.feature.rms(y=y))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))

    # Feature Vector
    feature_vector = [pauses, hesitations, speech_rate, pitch_var, energy, zcr]

    # Step 4: Anomaly Detection
    X = np.vstack([baseline_samples, feature_vector])
    clf = IsolationForest(contamination=0.2, random_state=42)
    clf.fit(X)

    risk_score = clf.decision_function([feature_vector])[0]
    at_risk = clf.predict([feature_vector])[0] == -1

    # Step 5: Plot pitch
    plot_name = f"static/pitch_{uuid.uuid4().hex}.png"
    plt.figure(figsize=(10, 4))
    plt.plot(pitch, color='purple')
    plt.title("Pitch Over Time")
    plt.xlabel("Frame")
    plt.ylabel("Pitch")
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.close()

    # Step 6: Return results
    return {
        "transcript": transcript,
        "features": {
            "Pauses": pauses,
            "Hesitations": hesitations,
            "Speech Rate (wpm)": round(speech_rate, 2),
            "Pitch Variability": round(pitch_var, 4),
            "Pitch Mean": round(pitch_mean, 2),
            "Energy (RMS)": round(energy, 4),
            "Zero Crossing Rate": round(zcr, 4),
            "Risk Score": round(risk_score, 2),
            "At Risk?": "Yes" if at_risk else "No"
        },
        "plot_path": "/" + plot_name
    }
