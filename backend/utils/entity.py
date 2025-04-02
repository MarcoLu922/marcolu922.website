import stanza

# 初始化 Stanza 中文 NLP 流水线（只启用分词和 NER）
# 建议在应用启动时初始化一次
nlp = stanza.Pipeline('zh', processors='tokenize,ner', verbose=False)

def extract_entities(text: str) -> list:
    """
    使用 Stanza 识别文本中的命名实体。
    返回格式为列表，每个实体为字典格式：{'text': ..., 'type': ...}
    """
    doc = nlp(text)
    entities = []
    for ent in doc.entities:
        entities.append({
            'text': ent.text,
            'type': ent.type  # 类型如 PERSON, LOCATION, ORGANIZATION 等
        })
    return entities
