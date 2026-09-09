# %%

import pandas as pd
import numpy as np
import sklearn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from nrclex import NRCLex
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

df = pd.read_csv(
    "hf://datasets/patrickbdevaney/tripadvisor_hotel_reviews/data/tripadvisor_hotel_reviews.csv"
)

analyser = SentimentIntensityAnalyzer()

df["score"] = np.nan
df["score"] = df["score"].astype("float64")

for index, series in df.iterrows():
    score = analyser.polarity_scores(str(series["Review"]))["compound"]
    df.loc[index, "score"] = score

df["sentiment"] = df["score"].apply(    
    lambda score: "Positive" if score > 0.05
    else "Negative" if score < -0.05
    else "Neutral"
)

# print(df)

# %%

sentiment_counts = df["sentiment"].value_counts()

labels = ["Positive", "Negative", "Neutral"]
sizes = [
    sentiment_counts.get("Positive", 0),
    sentiment_counts.get("Negative", 0),
    sentiment_counts.get("Neutral", 0)
]

total = sum(sizes)

colors = ["green", "red", "yellow"]

plt.figure(figsize=(9, 9))

wedges, _ = plt.pie(
    sizes,
    startangle=90,
    colors=colors
)

for i, wedge in enumerate(wedges):

    angle = (wedge.theta2 + wedge.theta1) / 2

    x = np.cos(np.deg2rad(angle))
    y = np.sin(np.deg2rad(angle))

    percentage = sizes[i] / total * 100

    text = f"{sizes[i]} ({percentage:.1f}%)"

    plt.annotate(
        text,
        xy=(x, y),
        xytext=(1.3 * x, 1.3 * y),
        ha="center",
        va="center",
        arrowprops=dict(
            arrowstyle="-",
            connectionstyle="arc3,rad=0.2"
        )
    )

plt.legend(
    wedges,
    labels,
    title="Sentiment",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

plt.tight_layout()
plt.show()

# %%

emotions = [
    "fear",
    "anger",
    "anticipation",
    "trust",
    "surprise",
    "positive",
    "negative",
    "sadness",
    "disgust",
    "joy"
]

emotion_totals = {
    "Positive": {emotion: 0 for emotion in emotions},
    "Negative": {emotion: 0 for emotion in emotions},
    "Neutral": {emotion: 0 for emotion in emotions}
}

for index, row in df.iterrows():

    review = str(row["Review"])
    sentiment = row["sentiment"]

    emotion = NRCLex()
    emotion.load_raw_text(review)

    scores = emotion.raw_emotion_scores

    for e in emotions:
        emotion_totals[sentiment][e] += scores.get(e, 0)

# %%

plt.figure(figsize=(12, 6))

plt.bar(
    emotion_totals["Positive"].keys(),
    emotion_totals["Positive"].values()
)

plt.title("Emotions in Positive Reviews")
plt.xlabel("Emotional Affect")
plt.ylabel("Emotion Score")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# %%

plt.figure(figsize=(12, 6))

plt.bar(
    emotion_totals["Negative"].keys(),
    emotion_totals["Negative"].values()
)

plt.title("Emotions in Negative Reviews")
plt.xlabel("Emotional Affect")
plt.ylabel("Emotion Score")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# %%

plt.figure(figsize=(12, 6))

plt.bar(
    emotion_totals["Neutral"].keys(),
    emotion_totals["Neutral"].values()
)

plt.title("Emotions in Neutral Reviews")
plt.xlabel("Emotional Affect")
plt.ylabel("Emotion Score")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# %%

df["rating_sentiment"] = df["Rating"].apply(
    lambda rating: "Positive" if rating >= 4
    else "Negative" if rating <= 2
    else "Neutral"
)

print(df[["Rating", "rating_sentiment"]].head())
# %%
labels = ["Negative", "Neutral", "Positive"]


cm = confusion_matrix(
    df["rating_sentiment"],
    df["sentiment"],
    labels=labels
)

print("===== Confusion Matrix =====")
print()

print("                 Review Sentiment")
print("              Negative  Neutral  Positive")

for i in range(len(labels)):
    print(
        f"{labels[i]:10}   "
        f"{cm[i][0]:8}  "
        f"{cm[i][1]:7}  "
        f"{cm[i][2]:8}"
    )

# Plot confusion matrix

plt.figure(figsize=(8, 6))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot()

plt.title("Rating Sentiment vs Review Sentiment")

plt.xlabel("Review Sentiment (VADER)")
plt.ylabel("Rating Sentiment")

plt.tight_layout()
plt.show()
# %%
