from backend.utils.entity import extract_entities
from backend.utils.intent import classify_intent
from backend.utils.sentiment import analyze_sentiment


def generate_dynamic_prompt(user_input: str, context: str, user_profile: dict = None) -> str:
    """
    构造动态 Prompt：
    - 包含历史对话上下文
    - 加入用户输入的意图、实体、情感分析结果
    - 可根据用户画像（暂时为空）调整回答风格
    """
    # 意图识别、实体抽取、情感分析
    intent = classify_intent(user_input)
    entities = extract_entities(user_input)
    sentiment, conf = analyze_sentiment(user_input)

    profile_info = user_profile.get("chat_summary", "暂无") if user_profile else "暂无"

    prompt = f"""
你是一名通用型的智能客服机器人，能够根据对话历史和当前输入生成准确、友好的回答。

【用户画像】：{profile_info}

【对话历史】：
{context}

【当前用户输入】：
原文：{user_input}
意图：{intent}
抽取的实体：{entities}
用户情感：{sentiment}（置信度 {conf:.2f}）

请基于以上信息给出详细、准确且符合通用客服风格的回答。
"""
    return prompt.strip()
