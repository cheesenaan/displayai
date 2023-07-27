import os
import openai

openai.api_key = os.getenv("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")
chatgptPrompt = '''give me a sample resume point'''
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": chatgptPrompt}
  ]
)
print(completion.choices[0].message.content)
