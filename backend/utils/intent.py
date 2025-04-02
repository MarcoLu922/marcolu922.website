def classify_intent(user_input: str) -> str:
    """
    基于关键词的简单意图识别。后续可用 Fine-tuned 模型替换。
    """
    text = user_input.lower()
    if "怎么" in text or "如何" in text:
        return "询问"
    elif "不满意" in text or "投诉" in text:
        return "投诉"
    else:
        return "一般"
