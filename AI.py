import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
sentences = [
    "I am thrilled with my new job", 
    "This is the worst day of my life", 
    "I am so grateful for my friends", 
    "I can't stand the traffic in this city", 
    "My vacation was absolutely amazing", 
    "I am extremely disappointed with the service", 
    "I love spending time with my family", 
    "This food tastes terrible", 
    "I am so happy with my progress", 
    "I regret buying this product"
]

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=tokenizer)

output = classifier(sentences)
print(output)

# inputs = tokenizer("I'm not sure whether my dog is cute or not", return_tensors="pt")
# with torch.no_grad():
#     logits = model(**inputs).logits

# predicted_class_id = logits.argmax().item()
# print(model.config.id2label[predicted_class_id])
