import pandas as pd
import matplotlib.pyplot as plt

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nrclex import NRCLex

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# ============================================================
# 1. LOAD TRAIN AND TEST DATA
# ============================================================

splits = {
    'train': 'train.jsonl',
    'test': 'test.jsonl'
}

train_df = pd.read_json(
    "hf://datasets/mteb/toxic_conversations_50k/" + splits["train"],
    lines=True
)

test_df = pd.read_json(
    "hf://datasets/mteb/toxic_conversations_50k/" + splits["test"],
    lines=True
)


# ============================================================
# 2. COMBINE TRAIN AND TEST DATA
# ============================================================

df = pd.concat([train_df, test_df], ignore_index=True)


# ============================================================
# 3. CREATE postText AND isToxic COLUMNS
# ============================================================

result_df = pd.DataFrame()

# Content from "text" goes to "postText"
result_df["postText"] = df["text"]

# label 1 = True (toxic)
# label 0 = False (not toxic)
result_df["isToxic"] = df["label"].astype(bool)


# ============================================================
# 4. VADER SENTIMENT ANALYSIS
# ============================================================

analyzer = SentimentIntensityAnalyzer()


def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


result_df["sentiment"] = result_df["postText"].apply(get_sentiment)


# ============================================================
# 5. NRCLEX EMOTION ANALYSIS
# ============================================================

def get_emotion(text):
    try:
        # Create NRCLex object WITHOUT passing empty string
        emotion = NRCLex()

        # Load the actual text
        emotion.load_raw_text(str(text))

        # Get raw emotion scores
        scores = emotion.raw_emotion_scores

        # Keep only the 8 NRC emotions
        valid_emotions = [
            "anger",
            "anticipation",
            "disgust",
            "fear",
            "joy",
            "sadness",
            "surprise",
            "trust"
        ]

        emotion_scores = {
            key: value
            for key, value in scores.items()
            if key in valid_emotions
        }

        # No emotion found
        if not emotion_scores:
            return "None"

        # Find the emotion with the highest score
        dominant_emotion = max(
            emotion_scores,
            key=emotion_scores.get
        )

        return dominant_emotion

    except Exception as e:
        print("NRCLex error:", e)
        return "None"


result_df["emotion"] = result_df["postText"].apply(get_emotion)


# ============================================================
# 6. SAVE THE CSV FILE
# ============================================================

result_df.to_csv(
    "2602-midisa.csv",
    index=False
)

print("CSV file created successfully.")
print("File: 2602-midisa.csv")


# ============================================================
# 7. DISPLAY FIRST FEW ROWS
# ============================================================

print("\nFirst 5 rows:")
print(result_df.head())


# ============================================================
# 8. CREATE DATA FOR CONFUSION MATRIX
# ============================================================

# Ground truth:
# True  = Toxic
# False = Not Toxic

y_true = result_df["isToxic"]


# Prediction:
# Negative sentiment = True
# Positive/Neutral sentiment = False

y_pred = result_df["sentiment"] == "Negative"


# ============================================================
# 9. CALCULATE CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_true,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# 10. DISPLAY CONFUSION MATRIX
# ============================================================

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Not Toxic", "Toxic"]
)

# Increased figure size
fig, ax = plt.subplots(figsize=(9, 7))

disp.plot(
    ax=ax,
    cmap="Blues",
    values_format="d"
)


# ============================================================
# 11. IMPROVE FONT SIZES AND SPACING
# ============================================================

# Increase title font size
plt.title(
    "Confusion Matrix: Toxicity vs VADER Sentiment",
    fontsize=16,
    pad=15
)

# X-axis label
plt.xlabel(
    "Predicted Class\nNegative Sentiment = Toxic",
    fontsize=13,
    labelpad=10
)

# Y-axis label
plt.ylabel(
    "Actual Class\nisToxic Ground Truth",
    fontsize=13,
    labelpad=10
)

# Increase tick label font size
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


# Increase numbers inside confusion matrix
for text in disp.text_.ravel():
    text.set_fontsize(13)


# ============================================================
# 12. ADD SEAT NUMBER
# ============================================================

seat_number = "2602"

plt.figtext(
    0.5,
    0.015,
    "Seat Number: " + seat_number,
    ha="center",
    fontsize=13
)


# ============================================================
# 13. ADJUST GRAPH SPACING
# ============================================================

plt.subplots_adjust(
    bottom=0.20,
    top=0.90,
    left=0.15,
    right=0.90
)


# ============================================================
# 14. SAVE CONFUSION MATRIX AS PNG
# ============================================================

plt.savefig(
    "2602-midisa.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nConfusion matrix image created successfully.")
print("File: 2602-midisa.png")