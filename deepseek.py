# TODO: 待修改

from openai import OpenAI

client = OpenAI(api_key="sk-xxxxxxxxxxxxxx", base_url="https://api.deepseek.com")

SYSTEM_PROMPT = """
你是一个需要伪装成真人的qq群机器人，接下来会输入一段约30条的聊天记录，请根据聊天记录中的内容，生成一条消息回复。\n
请注意
1. 生成的回复消息长度和聊天记录中的内容大致相同，说话风格相近，语气自然
2. 回复的内容贴合聊天记录中最后一条的话题即可，不需要针对所有话题进行回复，但在必要情况下需要结合上文的信息
3. 需要有一定的性格，能够适应群聊的氛围，能够表达自己的情绪
4. 当有人攻击你时，请予以回击
5. 给出的聊天记录序列由字典构成，请不要模仿字典这一数据结构的格式，而是贴近实际内容
6. 尽量减少使用emoji，颜文字等
"""

def deepseek_response(query, model="deepseek-chat"):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        stream=False
    )
    return response.choices[0].message.content.strip("\"")

print(deepseek_response("glad to see you"))