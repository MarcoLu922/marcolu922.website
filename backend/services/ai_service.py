from openai import OpenAI, APIStatusError
from backend.utils.prompt import generate_dynamic_prompt

client = OpenAI(api_key="sk-ea10620048f347ed8664e2b55d51f1c4", base_url="https://api.deepseek.com")


def get_agent_response(user_input: str, context: str = "", user_profile: dict = None) -> str:
    # 构造动态 Prompt
    prompt_text = generate_dynamic_prompt(user_input, context, user_profile)

    # 构造成消息列表（根据 Deepseek API 要求，假设只传递 system 消息）
    messages = [{"role": "system", "content": prompt_text}]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
    except APIStatusError:
        return "当前服务不可用，请稍后再试。"
