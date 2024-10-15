from openai import OpenAI

# APIキー
key = "YOUR_API_KEY"
# モデル
model = "gpt-4o-mini"
# トークンの最大長
max_tokens = 2048


service = OpenAI(api_key=key)

# 入力となる会話を格納するリスト
messages = []


# プロンプト
prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
messages.append({"role": "system", "content": prompt})

# ユーザからの発話
# messages.append({"role": "user", "content": "GPT はときどき嘘をつきますね。"})
# messages.append({"role": "user", "content": "反省していますか?"})
messages.append(
    {"role": "user", "content": "日本語の動詞の活用型をすべて教えてください。"}
)

# 入力の確認
for message in messages:
    print(f"{message.get('role')}: {message.get('content')}")


# 会話の取得
completionResult = service.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=max_tokens,
)
choiceList = completionResult.choices

# 会話の表示
for choice in choiceList:
    chatMessage = choice.message
    print(f"{chatMessage.role}: {chatMessage.content}")
