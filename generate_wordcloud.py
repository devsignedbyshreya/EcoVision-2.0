from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import random
import re
import os
from collections import Counter

# Load dataset
df = pd.read_csv("data/Final_Dataset.csv")

# Create output folder
os.makedirs("static/images", exist_ok=True)

# Combine all text
all_text = " ".join(
    df["text"].astype(str)
)

# Lowercase
all_text = all_text.lower()

# Remove URLs
all_text = re.sub(r"http\S+", "", all_text)

# Remove emails
all_text = re.sub(r"\S+@\S+", "", all_text)

# Keep only letters
all_text = re.sub(r"[^a-z\s]", " ", all_text)

# Remove extra spaces
all_text = re.sub(r"\s+", " ", all_text)

# Tokenize
words = all_text.split()

# Strong stopword list
custom_stopwords = set(STOPWORDS)

custom_stopwords.update([

    # Generic news words
    "said", "will", "also", "one", "two", "new",
    "year", "years", "people", "government",
    "countries", "country", "world", "global",
    "news", "article", "report", "reported",

    # Garbage tokens
    "la", "re", "se", "u", "ga", "que",
    "en", "de", "el", "un", "una", "los",
    "del", "con", "para", "por", "du",

    # Generic verbs
    "make", "take", "need", "use", "used",
    "using", "work", "working", "see", "know",

    # Misc noise
    "could", "would", "may", "might", "even",
    "many", "much", "still", "now", "first",
    "last", "around", "across", "including"
])

# Keep meaningful words only
filtered_words = [

    word for word in words

    if (
        len(word) > 3
        and word not in custom_stopwords
    )
]

# Frequency filtering
word_freq = Counter(filtered_words)

# Remove ultra-common noisy words
filtered_freq = {

    word: freq

    for word, freq in word_freq.items()

    if freq > 8
}

# SDG Colors
sdg_colors = [
    "#E5243B",
    "#DDA63A",
    "#4C9F38",
    "#C5192D",
    "#FF3A21",
    "#26BDE2",
    "#FCC30B",
    "#A21942",
    "#FD6925",
    "#DD1367",
    "#FD9D24",
    "#BF8B2E",
    "#3F7E44",
    "#0A97D9",
    "#56C02B",
    "#00689D",
    "#19486A"
]

# Generate cloud
wordcloud = WordCloud(
    width=1800,
    height=900,
    background_color="#ffffff",
    max_words=180,
    collocations=False
).generate_from_frequencies(filtered_freq)

# Color function
def color_func(*args, **kwargs):
    return random.choice(sdg_colors)

# Plot
plt.figure(figsize=(18, 9), facecolor="#0f172a")

plt.imshow(
    wordcloud.recolor(color_func=color_func),
    interpolation="bilinear"
)

plt.axis("off")


# Save
save_path = "static/images/wordcloud_research.png"

plt.savefig(
    save_path,
    bbox_inches="tight",
    dpi=300,
    facecolor="#ffffff"
)

plt.close()

print(f"Saved -> {save_path}")