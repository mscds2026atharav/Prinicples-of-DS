import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nrclex import NRCLex
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Sentiment & Coursera Dashboard",
    layout="wide"
)

# LOAD TRIPADVISOR DATA
@st.cache_data
def load_tripadvisor_data():

    df = pd.read_csv(
        "hf://datasets/patrickbdevaney/tripadvisor_hotel_reviews/data/tripadvisor_hotel_reviews.csv"
    )

    analyser = SentimentIntensityAnalyzer()

    # Calculate VADER sentiment score
    df["score"] = df["Review"].apply(
        lambda review:
        analyser.polarity_scores(str(review))["compound"]
    )

    # Convert score into sentiment
    df["sentiment"] = df["score"].apply(
        lambda score:
        "Positive" if score > 0.05
        else "Negative" if score < -0.05
        else "Neutral"
    )

    # Convert rating into sentiment
    df["rating_sentiment"] = df["Rating"].apply(
        lambda rating:
        "Positive" if rating >= 4
        else "Negative" if rating <= 2
        else "Neutral"
    )

    return df

# CALCULATE NRC EMOTIONS
@st.cache_data
def calculate_emotions(df):

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

    for _, row in df.iterrows():

        review = str(row["Review"])
        sentiment = row["sentiment"]

        emotion = NRCLex()
        emotion.load_raw_text(review)

        scores = emotion.raw_emotion_scores

        for e in emotions:

            emotion_totals[sentiment][e] += scores.get(e, 0)

    return emotion_totals, emotions


# LOAD COURSERA JSON
@st.cache_data
def load_coursera_data():

    # app.py is inside WebDashboard
    # .parent goes to the main project folder
    project_folder = Path(__file__).parent.parent

    json_file = project_folder / "coursera_courses.json"

    try:

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return pd.DataFrame(data)

    except FileNotFoundError:

        st.error(
            f"Could not find the JSON file at:\n{json_file}"
        )

        return pd.DataFrame()
# LOAD DATA
df = load_tripadvisor_data()

emotion_totals, emotions = calculate_emotions(df)

coursera_df = load_coursera_data()


# SIDEBAR NAVIGATION
# TOP NAVIGATION

st.title("Data Analysis Dashboard")

page = st.radio(
    "Navigation",
    [
        "Sentiment & Rating Analysis",
        "Coursera Courses"
    ],
    horizontal=True
)

st.divider()


# PAGE 1
# SENTIMENT & RATING ANALYSIS
if page == "Sentiment & Rating Analysis":

    st.title("Sentiment & Rating Analysis")

    st.markdown(
        "Analysis of TripAdvisor hotel reviews using "
        "VADER sentiment analysis and NRC emotion analysis."
    )

    st.divider()


    # SECTION 1 — SENTIMENT OVERVIEW
    st.header("1. Sentiment Distribution")

    sentiment_counts = df["sentiment"].value_counts()

    labels = [
        "Positive",
        "Negative",
        "Neutral"
    ]

    sizes = [
        sentiment_counts.get("Positive", 0),
        sentiment_counts.get("Negative", 0),
        sentiment_counts.get("Neutral", 0)
    ]

    total = sum(sizes)

    colors = [
        "green",
        "red",
        "yellow"
    ]

    fig, ax = plt.subplots(
        figsize=(9, 7)
    )

    wedges, _ = ax.pie(
        sizes,
        startangle=90,
        colors=colors
    )

    # Add count and percentage outside pie
    for i, wedge in enumerate(wedges):

        angle = (
            wedge.theta2 + wedge.theta1
        ) / 2

        x = np.cos(
            np.deg2rad(angle)
        )

        y = np.sin(
            np.deg2rad(angle)
        )

        percentage = (
            sizes[i] / total * 100
        )

        text = (
            f"{sizes[i]} "
            f"({percentage:.1f}%)"
        )

        ax.annotate(
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

    ax.legend(
        wedges,
        labels,
        title="Sentiment",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    st.pyplot(fig)

    st.divider()


    # SECTION 2 — EMOTION ANALYSIS
    st.header("2. Emotion Analysis")

    st.markdown(
        "NRC Lex emotion scores grouped according to "
        "the VADER sentiment of the review."
    )

    # Positive emotions
    st.subheader("Positive Reviews")

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.bar(
        emotion_totals["Positive"].keys(),
        emotion_totals["Positive"].values()
    )

    ax.set_title(
        "Emotions in Positive Reviews"
    )

    ax.set_xlabel(
        "Emotional Affect"
    )

    ax.set_ylabel(
        "Emotion Score"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig)

    # Negative emotions
    st.subheader("Negative Reviews")

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.bar(
        emotion_totals["Negative"].keys(),
        emotion_totals["Negative"].values()
    )

    ax.set_title(
        "Emotions in Negative Reviews"
    )

    ax.set_xlabel(
        "Emotional Affect"
    )

    ax.set_ylabel(
        "Emotion Score"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig)

    # Neutral emotions
    st.subheader("Neutral Reviews")

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.bar(
        emotion_totals["Neutral"].keys(),
        emotion_totals["Neutral"].values()
    )

    ax.set_title(
        "Emotions in Neutral Reviews"
    )

    ax.set_xlabel(
        "Emotional Affect"
    )

    ax.set_ylabel(
        "Emotion Score"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig)

    st.divider()

    # SECTION 3 — RATING SENTIMENT
    st.header("3. Rating vs Review Sentiment")

    st.markdown(
        """
        **Rating mapping:**

        - 1–2 ⭐ → Negative
        - 3 ⭐ → Neutral
        - 4–5 ⭐ → Positive
        """
    )

    # Rating sentiment counts
    review_counts = (
        df["sentiment"]
        .value_counts()
        .reindex(
            ["Positive", "Negative", "Neutral"],
            fill_value=0
        )
    )

    rating_counts = (
        df["rating_sentiment"]
        .value_counts()
        .reindex(
            ["Positive", "Negative", "Neutral"],
            fill_value=0
        )
    )


    comparison_df = pd.DataFrame({
        "Review Sentiment": review_counts,
        "Rating Sentiment": rating_counts
    })


    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    x = np.arange(3)

    width = 0.35

    ax.bar(
        x - width / 2,
        comparison_df["Review Sentiment"],
        width,
        label="Review Sentiment"
    )

    ax.bar(
        x + width / 2,
        comparison_df["Rating Sentiment"],
        width,
        label="Rating Sentiment"
    )

    ax.set_xticks(x)

    ax.set_xticklabels(
        [
            "Positive",
            "Negative",
            "Neutral"
        ]
    )

    ax.set_ylabel("Number of Reviews")

    ax.set_title(
        "Review Sentiment vs Rating Sentiment"
    )

    ax.legend()

    plt.tight_layout()

    st.pyplot(fig)

    # Difference in counts
    st.subheader("Difference in Counts")

    difference_df = pd.DataFrame({
        "Review Sentiment Count":
            review_counts,

        "Rating Sentiment Count":
            rating_counts
    })

    difference_df["Difference"] = (
        difference_df["Review Sentiment Count"]
        -
        difference_df["Rating Sentiment Count"]
    )

    st.dataframe(
        difference_df,
        use_container_width=True
    )

    st.divider()

    # SECTION 4 — CONFUSION MATRIX
    st.header("4. Confusion Matrix")

    labels = [
        "Negative",
        "Neutral",
        "Positive"
    ]

    cm = confusion_matrix(
        df["rating_sentiment"],
        df["sentiment"],
        labels=labels
    )

    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=labels
    )

    disp.plot(
        ax=ax
    )

    ax.set_title(
        "Rating Sentiment vs Review Sentiment"
    )

    ax.set_xlabel(
        "Review Sentiment (VADER)"
    )

    ax.set_ylabel(
        "Rating Sentiment"
    )

    plt.tight_layout()

    st.pyplot(fig)

    # SECTION 5 — RAW DATA
    st.divider()

    st.header("5. Dataset")

    st.write(
        f"Total reviews: **{len(df)}**"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# PAGE 2
# PAGE 2
# COURSERA COURSES
elif page == "Coursera Courses":

    st.title("Coursera Course Analysis")

    st.markdown(
        "Analysis of the courses collected using the "
        "BeautifulSoup web scraper."
    )

    st.divider()


    if coursera_df.empty:

        st.error(
            "coursera_courses.json was not found "
            "or contains no courses."
        )

        st.info(
            "Make sure coursera_courses.json is "
            "available in the project folder."
        )

    else:

        # ====================================================
        # CLEAN DATA
        # ====================================================

        coursera_df["rating_score"] = pd.to_numeric(
            coursera_df["rating_score"],
            errors="coerce"
        )

        rated_courses = coursera_df.dropna(
            subset=["rating_score"]
        )


        # ====================================================
        # 1. TOP 3 COURSES BY RATING
        # ====================================================

        st.header("1. Top 3 Courses by Rating")

        top_3 = (
            rated_courses
            .sort_values(
                by="rating_score",
                ascending=False
            )
            .head(3)
        )

        cols = st.columns(3)

        for i, (_, course) in enumerate(
            top_3.iterrows()
        ):

            with cols[i]:

                st.subheader(
                    f"#{i + 1}"
                )

                st.markdown(
                    f"**{course['course_name']}**"
                )

                st.write(
                    f"**Organization:** "
                    f"{course['organization_name']}"
                )

                st.metric(
                    "Rating",
                    f"⭐ {course['rating_score']:.1f}"
                )

                st.write(
                    f"**Level:** "
                    f"{course['course_level']}"
                )

                st.write(
                    f"**Type:** "
                    f"{course['course_type']}"
                )

                st.write(
                    f"**Duration:** "
                    f"{course['duration']}"
                )


        st.divider()

        # ====================================================
        # 4. COURSE LEVEL DISTRIBUTION
        # ====================================================

        st.header("4. Course Level Distribution")

        level_counts = (
            coursera_df[
                "course_level"
            ]
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(8, 7)
        )

        wedges, texts, autotexts = ax.pie(
            level_counts.values,
            labels=level_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Distribution of Courses by Level"
        )

        plt.tight_layout()

        st.pyplot(fig)

        st.info(
            "Beginner vs Intermediate vs Advanced"
        )


        st.divider()


        # ====================================================
        # 5. COURSE DATA
        # ====================================================

        st.header("5. Course Data")

        st.dataframe(
            coursera_df,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # 6. RAW JSON
        # ====================================================

        st.divider()

        st.header("6. Raw JSON")

        st.json(
            coursera_df.to_dict(
                orient="records"
            )
        )