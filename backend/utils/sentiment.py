from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis", model="uer/roberta-base-finetuned-jd-binary-chinese")

def analyze_sentiment(user_input: str) -> (str, float):
    result = sentiment_analyzer(user_input)
    label = result[0]["label"]  # LABEL_0 或 LABEL_1，具体模型的输出可能不同
    score = result[0]["score"]
    # 假设 LABEL_0 表示负面，LABEL_1 表示正面
    sentiment = "负面" if label == "LABEL_0" else "正面"
    return sentiment, score
