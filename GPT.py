import requests
import json

class GPT:

    @staticmethod
    def GET_ANS_TEST(MSG):
        LIN = ""
        for i in range(48, 16 + 48):
            C = chr(i)
            LIN += C + ","
        LIN = LIN[:-1]
        return LIN

    @staticmethod
    def GET_ANS_TEST_DEG(MSG):
        return "B.S."

    @staticmethod
    def GET_ANS_TEST_PAY(MSG):
        return "79000"

    @staticmethod
    def GET_ANS_TEST_X(MSG):
        return "ABCXYZ"

    @staticmethod
    def GET_ANS(MSG):
        url = "https://api.openai.com/v1/chat/completions"
        apiKey = ""  # API key goes here
        model = "gpt-3.5-turbo"  # current model of chatgpt api

        try:
            headers = {
                "Authorization": f"Bearer {apiKey}",
                "Content-Type": "application/json"
            }

            temperature = 0.2
            body = json.dumps({
                "model": model,
                "temperature": temperature,
                "messages": [{"role": "user", "content": MSG}]
            })

            response = requests.post(url, headers=headers, data=body)
            response.raise_for_status()
            return GPT.EXT(response.text)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(e)

    @staticmethod
    def EXT(ANS):
        start_idx = ANS.find("content") + 11
        end_idx = ANS.find("\"", start_idx)
        return ANS[start_idx:end_idx]