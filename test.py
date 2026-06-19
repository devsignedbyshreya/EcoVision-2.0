from transformers import AutoModelForSequenceClassification

print("loading...")
model = AutoModelForSequenceClassification.from_pretrained("model")
print("done")