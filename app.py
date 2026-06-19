from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import pandas as pd
import os
import re
from collections import Counter
from deep_translator import GoogleTranslator
from langdetect import detect

app = Flask(__name__)

# MODEL_PATH = "model"
# DATASET_FILE = r"C:\Personal\SDG_News_classifier\UI\data\Final_Dataset.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODEL_PATH = os.path.join(BASE_DIR, "model")
SDG_MODEL_PATH = "devsignedbyshreya/ecovision-sdg-model"

SENTIMENT_MODEL_PATH = "devsignedbyshreya/ecovision-sentiment-model"
DATASET_FILE = os.path.join(BASE_DIR, "data", "Final_Dataset.csv")

# print("Starting app...")
# print("Loading tokenizer...")
# # tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
# tokenizer = AutoTokenizer.from_pretrained(
#     SDG_MODEL_PATH,
#     use_fast=False
# )

# print("Loading model...")
# # model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# device = torch.device("cpu")
# print("Moving model to device...")
# model.to(device)
# model.eval()
# print("Model loaded successfully!")
print("Starting app...")

print("Loading SDG tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    SDG_MODEL_PATH,
    use_fast=False
)

print("Loading SDG model...")

model = AutoModelForSequenceClassification.from_pretrained(
    SDG_MODEL_PATH
)

device = torch.device("cpu")

print("Moving model to device...")

model.to(device)

model.eval()

print("SDG Model loaded successfully!")
print("Loading Sentiment tokenizer...")

sentiment_tokenizer = AutoTokenizer.from_pretrained(
    SENTIMENT_MODEL_PATH,
    use_fast=False
)

print("Loading Sentiment model...")

sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    SENTIMENT_MODEL_PATH
)

sentiment_model.to(device)

sentiment_model.eval()

print("Sentiment Model loaded successfully!")
sdg_names = {
    0: "SDG 1 - No Poverty",
    1: "SDG 2 - Zero Hunger",
    2: "SDG 3 - Good Health and Well-being",
    3: "SDG 4 - Quality Education",
    4: "SDG 5 - Gender Equality",
    5: "SDG 6 - Clean Water and Sanitation",
    6: "SDG 7 - Affordable and Clean Energy",
    7: "SDG 8 - Decent Work and Economic Growth",
    8: "SDG 9 - Industry, Innovation and Infrastructure",
    9: "SDG 10 - Reduced Inequalities",
    10: "SDG 11 - Sustainable Cities and Communities",
    11: "SDG 12 - Responsible Consumption and Production",
    12: "SDG 13 - Climate Action",
    13: "SDG 14 - Life Below Water",
    14: "SDG 15 - Life on Land",
    15: "SDG 16 - Peace, Justice and Strong Institutions",
    16: "SDG 17 - Partnerships for the Goals"
}
sentiment_labels = {
    1: "Negative",
    0: "Neutral",
    2: "Positive"
}

STOPWORDS = {
    "will","a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves","also", "however", "therefore", "thus", "hence", "moreover", "furthermore", "meanwhile", "although", "though", "whereas", "while", "because", "since", "unless", "until", "whether", "despite", "besides", "within", "without", "across", "behind", "beyond", "beneath", "beside", "upon", "among", "throughout","just", "even", "still", "yet", "already", "again", "ever", "never", "always", "sometimes", "often", "usually", "really", "quite", "rather", "very", "too", "much", "many", "few", "little", "enough", "more", "most", "less", "least","one", "two", "three", "first", "second", "third", "next", "last", "another", "several", "various", "many", "much", "few", "little","say", "says", "said", "go", "goes", "went", "gone", "make", "makes", "made", "take", "takes", "took", "taken", "come", "comes", "came", "get", "gets", "got", "gotten", "see", "sees", "saw", "seen", "know", "knows", "knew", "known", "think", "thinks", "thought","use", "used", "using", "want", "wants", "wanted", "give", "gives", "gave", "given", "find", "finds", "found", "tell", "tells", "told", "ask", "asks", "asked", "work", "works", "worked", "working", "try", "tries", "tried","thing", "things", "something", "anything", "nothing", "everything", "someone", "anyone", "everyone", "noone", "none", "somewhere", "anywhere", "everywhere","data", "information", "system", "systems", "process", "processes", "method", "methods", "model", "models", "result", "results", "example", "examples", "case", "cases", "study", "studies", "research", "paper", "article", "report","etc", "ie", "eg", "via", "per", "vs", "such", "like", "including", "includes", "included", "based", "according", "related", "relevant", "important", "significant", "different", "similar", "same", "general", "specific"
}

def clean_words(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    words = [w for w in text.split() if len(w) > 2 and w not in STOPWORDS]
    return words
def translate_to_english(text):

    try:

        language = detect(text)

        print("Detected Language:", language)

        if language != "en":

            translated = GoogleTranslator(
                source='auto',
                target='en'
            ).translate(text)

            return translated

        return text

    except Exception as e:

        print("Translation Error:", e)

        return text
    
def predict_sdg(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)[0]

    top3_probs, top3_ids = torch.topk(probs, k=3)
    pred_id = top3_ids[0].item()

    top3_predictions = []
    for idx, prob in zip(top3_ids.tolist(), top3_probs.tolist()):
        top3_predictions.append({
            "label": sdg_names[idx],
            "confidence": round(float(prob), 4)
        })

    return {
        "predicted_label": sdg_names[pred_id],
        "top3_predictions": top3_predictions
    }

def predict_sentiment(text):

    inputs = sentiment_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        outputs = sentiment_model(**inputs)

        probs = F.softmax(
            outputs.logits,
            dim=1
        )[0]

    pred_id = torch.argmax(probs).item()

    confidence = probs[pred_id].item()

    print("Sentiment Prediction:", pred_id)

    print("Confidence:", confidence)

    return {
        "label": sentiment_labels[pred_id],
        "confidence": round(confidence * 100, 2)
    }

def load_dashboard_data():
    print("Looking for dataset at:", DATASET_FILE)

    if not os.path.exists(DATASET_FILE):
        raise FileNotFoundError(f"Dataset file not found: {DATASET_FILE}")

    df = pd.read_csv(DATASET_FILE)
    df.columns = df.columns.str.strip()

    numeric_cols = ["top1_conf", "top2_conf", "top3_conf", "word_count", "text_length", "confidence"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def apply_filters(df):
    temp = df.copy()

    sdg = request.args.get("sdg")
    min_conf = request.args.get("min_conf", type=float)

    if sdg and "primary_sdg" in temp.columns:
        temp = temp[temp["primary_sdg"].astype(str) == sdg]

    if min_conf is not None and "top1_conf" in temp.columns:
        temp = temp[temp["top1_conf"] >= min_conf]

    return temp

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sdgs")
def sdgs():
    return render_template("sdgs.html")

@app.route("/classifier", methods=["GET", "POST"])
def classifier():
    prediction = None
    top3_predictions = None

    sentiment = None
    sentiment_confidence = None

    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("news_text", "").strip()
        if input_text:

            try:

                # Translate text to English if needed
                translated_text = translate_to_english(input_text)

                print("Translated Text:", translated_text)

                # SDG prediction
                result = predict_sdg(translated_text)

                prediction = result["predicted_label"]

                top3_predictions = result["top3_predictions"]

                # Sentiment prediction
                sentiment_result = predict_sentiment(translated_text)

                print("Sentiment Result:", sentiment_result)

                sentiment = sentiment_result["label"]

                sentiment_confidence = sentiment_result["confidence"]

                print("Sentiment:", sentiment)

                print("Confidence:", sentiment_confidence)

            except Exception as e:

                print("ERROR IN PREDICTION:", e)

    return render_template(
        "classifier.html",

        prediction=prediction,

        top3_predictions=top3_predictions,

        sentiment=sentiment,

        sentiment_confidence=sentiment_confidence,

        input_text=input_text
    )

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/research")
def research():
    return render_template("research.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api/debug-dataset")
def api_debug_dataset():
    try:
        df = load_dashboard_data()
        return jsonify({
            "status": "ok",
            "shape": [int(df.shape[0]), int(df.shape[1])],
            "columns": [str(c) for c in df.columns.tolist()],
            "head": df.head(2).fillna("").astype(object).to_dict(orient="records")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/filter-options")
def api_filter_options():
    try:
        df = load_dashboard_data()

        sdgs = []
        if "primary_sdg" in df.columns:
            raw_sdgs = df["primary_sdg"].dropna().astype(str).unique().tolist()

            def sdg_sort_key(x):
                match = re.search(r"\d+", x)
                return int(match.group()) if match else 999

            sdgs = sorted(raw_sdgs, key=sdg_sort_key)

        return jsonify({
            "sdgs": sdgs,
            "sources": ["All Data"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/summary")
def api_summary():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        if temp.empty:
            return jsonify({
                "total_articles": 0,
                "avg_confidence": 0.0,
                "top_sdg": "N/A",
                "avg_word_count": 0.0
            })

        total_articles = int(len(temp))

        highest_conf = 0.0
        if "top1_conf" in temp.columns:
            highest_conf = float(temp["top1_conf"].dropna().max()) * 100

        avg_word_count = 0.0
        if "word_count" in temp.columns:
            avg_word_count = float(temp["word_count"].dropna().mean())

        top_sdg = (
            str(temp["primary_sdg"].mode().iloc[0])
            if "primary_sdg" in temp.columns and not temp["primary_sdg"].mode().empty
            else "N/A"
        )

        return jsonify({
            "total_articles": total_articles,
            "avg_confidence": round(highest_conf, 2),
            "top_sdg": top_sdg,
            "avg_word_count": round(avg_word_count, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sdg-distribution")
def api_sdg_distribution():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        if temp.empty or "primary_sdg" not in temp.columns:
            return jsonify({"labels": [], "values": []})

        counts = temp["primary_sdg"].value_counts()

        def sdg_sort_key(x):
            match = re.search(r"\d+", str(x))
            return int(match.group()) if match else 999

        counts = counts.reindex(sorted(counts.index.tolist(), key=sdg_sort_key))

        return jsonify({
            "labels": [str(x) for x in counts.index.tolist()],
            "values": [int(x) for x in counts.values.tolist()]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/confidence-by-sdg")
def api_confidence_by_sdg():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        if temp.empty or "primary_sdg" not in temp.columns or "top1_conf" not in temp.columns:
            return jsonify({"labels": [], "values": []})

        grouped = temp.groupby("primary_sdg")["top1_conf"].mean()

        def sdg_sort_key(x):
            match = re.search(r"\d+", str(x))
            return int(match.group()) if match else 999

        ordered_index = sorted(grouped.index.tolist(), key=sdg_sort_key)
        grouped = grouped.reindex(ordered_index)

        return jsonify({
            "labels": [str(x) for x in grouped.index.tolist()],
            "values": [float(round(x, 4)) for x in grouped.values.tolist()]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/heatmap")
def api_heatmap():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        if temp.empty or "top1_sdg" not in temp.columns or "top2_sdg" not in temp.columns:
            return jsonify({"x": [], "y": [], "z": []})

        matrix = pd.crosstab(temp["top1_sdg"], temp["top2_sdg"])

        # keep only SDGs that actually matter visually
        row_sums = matrix.sum(axis=1).sort_values(ascending=False)
        top_rows = row_sums.head(8).index
        matrix = matrix.loc[top_rows]

        col_sums = matrix.sum(axis=0).sort_values(ascending=False)
        top_cols = col_sums.head(8).index
        matrix = matrix[top_cols]

        return jsonify({
            "x": [str(x) for x in matrix.columns.tolist()],
            "y": [str(y) for y in matrix.index.tolist()],
            "z": [[int(v) for v in row] for row in matrix.values.tolist()]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/scatter")
def api_scatter():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        needed = ["word_count", "top1_conf", "primary_sdg"]
        if temp.empty or any(col not in temp.columns for col in needed):
            return jsonify({
                "x": [],
                "y": [],
                "labels": [],
                "titles": []
            })

        temp = temp.dropna(subset=needed).copy()

        if len(temp) > 1200:
            temp = temp.sample(1200, random_state=42)

        titles = temp["title"].fillna("").astype(str).tolist() if "title" in temp.columns else [""] * len(temp)

        return jsonify({
            "x": [int(x) for x in temp["word_count"].tolist()],
            "y": [float(y) for y in temp["top1_conf"].tolist()],
            "labels": temp["primary_sdg"].astype(str).tolist(),
            "titles": titles
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/top-keywords")
def api_top_keywords():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        if temp.empty:
            return jsonify({"labels": [], "values": []})

        if "text" in temp.columns:
            combined_text = " ".join(temp["text"].fillna("").astype(str))
        elif "article_text" in temp.columns:
            combined_text = " ".join(temp["article_text"].fillna("").astype(str))
        else:
            return jsonify({"labels": [], "values": []})

        words = clean_words(combined_text)
        freq = Counter(words).most_common(10)

        return jsonify({
            "labels": [str(word) for word, _ in freq],
            "values": [int(count) for _, count in freq]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/articles")
def api_articles():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        cols = ["title", "primary_sdg", "top1_conf", "top2_sdg", "top2_conf", "word_count"]
        available_cols = [col for col in cols if col in temp.columns]

        if temp.empty or not available_cols:
            return jsonify([])

        temp = temp[available_cols].copy().head(50)
        temp = temp.fillna("").astype(object)

        return jsonify(temp.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/wordcloud")
def api_wordcloud():
    try:
        df = load_dashboard_data()
        temp = apply_filters(df)

        if temp.empty:
            return jsonify([])

        if "text" in temp.columns:
            combined_text = " ".join(temp["text"].fillna("").astype(str))
        elif "article_text" in temp.columns:
            combined_text = " ".join(temp["article_text"].fillna("").astype(str))
        else:
            return jsonify([])

        words = clean_words(combined_text)
        freq = Counter(words).most_common(60)

        return jsonify([
            {"text": str(word), "value": int(count)}
            for word, count in freq
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/api/sentiment-distribution")
def api_sentiment_distribution():

    return jsonify({

        "labels": [
            "Negative",
            "Positive",
            "Neutral"
        ],

        "values": [
            9558,   
            9093,   
            4663
        ]
    })

@app.route('/api/ml-vs-dl')
def ml_vs_dl():

    metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]

    ml_scores = [0.89, 0.88, 0.87, 0.88]

    dl_scores = [0.94, 0.93, 0.94, 0.93]

    return jsonify({
        "metrics": metrics,
        "ml_scores": ml_scores,
        "dl_scores": dl_scores
    })
    
@app.route("/test-sentiment")
def test_sentiment():

    text = "Renewable energy investments are improving global employment."

    result = predict_sentiment(text)

    return str(result)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)