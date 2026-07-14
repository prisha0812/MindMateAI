import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from emotion import detect_emotion

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("emotion_test_dataset.csv")

true_labels = []
predicted_labels = []
confidence_scores = []

for _, row in df.iterrows():

    emotion, confidence = detect_emotion(row["text"])

    true_labels.append(row["label"])
    predicted_labels.append(emotion)
    confidence_scores.append(confidence)

# ==========================
# Save Predictions
# ==========================

results = df.copy()
results["predicted"] = predicted_labels
results["confidence"] = confidence_scores

results.to_csv("prediction_results.csv", index=False)

# ==========================
# Metrics
# ==========================

accuracy = accuracy_score(true_labels, predicted_labels)

precision = precision_score(
    true_labels,
    predicted_labels,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    true_labels,
    predicted_labels,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    true_labels,
    predicted_labels,
    average="weighted",
    zero_division=0
)

print("\nAccuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

# ==========================
# Classification Report
# ==========================

report = classification_report(
    true_labels,
    predicted_labels,
    output_dict=True,
    zero_division=0
)

pd.DataFrame(report).transpose().to_csv(
    "classification_report.csv"
)

# ==========================
# Misclassified Samples
# ==========================

mistakes = results[
    results["label"] != results["predicted"]
]

mistakes.to_csv(
    "misclassified_samples.csv",
    index=False
)

# ==========================
# Confusion Matrix
# ==========================

labels = [
    "anger",
    "disgust",
    "fear",
    "joy",
    "neutral",
    "sadness",
    "surprise"
]

cm = confusion_matrix(
    true_labels,
    predicted_labels,
    labels=labels
)

plt.figure(figsize=(8,6))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=labels,
    yticklabels=labels
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.savefig(
    "confusion_matrix.png",
    dpi=300
)

plt.close()

# ==========================
# Metrics Plot
# ==========================

metrics = [accuracy, precision, recall, f1]
names = ["Accuracy","Precision","Recall","F1 Score"]

plt.figure(figsize=(6,5))

bars = plt.bar(names, metrics)

for bar in bars:
    y = bar.get_height()
    plt.text(
        bar.get_x()+bar.get_width()/2,
        y+0.01,
        f"{y:.2f}",
        ha="center"
    )

plt.ylim(0,1.05)

plt.title("Model Performance")

plt.savefig(
    "performance_metrics.png",
    dpi=300
)

plt.close()

print("\nGenerated Files:")
print("- prediction_results.csv")
print("- classification_report.csv")
print("- misclassified_samples.csv")
print("- confusion_matrix.png")
print("- performance_metrics.png")