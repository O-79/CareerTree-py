import os
from openai import OpenAI

class GPT:
    @staticmethod
    def GET_ANS(MSG):
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI()
        
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            temperature = 0.1,
            top_p = 0.1,
            messages = [
                {"role": "user", "content": MSG}
            ]
        )
        
        return completion.choices[0].message.content.strip()