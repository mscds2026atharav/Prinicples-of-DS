from nrclex import NRCLex

text = "I am extremely happy and joyful today!"

emotion = NRCLex()

emotion.load_raw_text(text)

print("Raw emotion scores:")
print(emotion.raw_emotion_scores)

print("\nTop emotions:")
print(emotion.top_emotions)