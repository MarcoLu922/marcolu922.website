from transformers import pipeline

# 加载 T5/BART 预训练模型进行摘要
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_context(context_text, max_length=500):
    """
    采用 NLP 模型对超长上下文进行摘要。
    """
    if len(context_text) > max_length:
        summary = summarizer(context_text, max_length=max_length//2, min_length=50, do_sample=False)[0]["summary_text"]
        summary += "\n...[摘要了剩余部分]..."
        return summary
    return context_text

def update_context(existing_context, user_input, agent_response, max_total_length=2000):
    """
    将用户输入和代理回复追加到现有上下文中，
    并在总长度超过 max_total_length 时，对旧内容进行摘要处理。
    """
    # 构造新的对话记录格式（每一轮以 "User:" 和 "Agent:" 开头）
    new_entry = f"User: {user_input}\nAgent: {agent_response}\n"
    new_context = existing_context + new_entry

    # 如果新上下文超过设定的最大长度，则对整个上下文进行摘要
    if len(new_context) > max_total_length:
        new_context = summarize_context(new_context, max_length=max_total_length//2)
        # 可选：将最新的一轮对话追加上去（如果摘要后希望保留最新消息）
        new_context += new_entry

    return new_context
