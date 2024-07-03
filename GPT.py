import requests
import json

class GPT:
    with open('key.txt', 'r') as f:
        KEY = f.read().strip()
        f.close()

    @staticmethod
    def GET_ANS_TEST(MSG):
        return GPT.GET_ANS(MSG)
        # LIN = ""
        # for i in range(48, 16 + 48):
        #     C = chr(i)
        #     LIN += C + ","
        # LIN = LIN[:-1]

    @staticmethod
    def GET_ANS_TEST_DEG(MSG):
        return GPT.GET_ANS(MSG)
        # return "B.S."

    @staticmethod
    def GET_ANS_TEST_PAY(MSG):
        return GPT.GET_ANS(MSG)
        # return "79000"

    @staticmethod
    def GET_ANS_TEST_X(MSG):
        return GPT.GET_ANS(MSG)
        # return "ABCXYZ"

    @staticmethod
    def GET_ANS(MSG):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = GPT.KEY
        model = "gpt-3.5-turbo"

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
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
            
            response_data = response.json()
            
            choice = response_data['choices']
            within_choice = choice[0]
            message = within_choice['message']
            content = message['content']
            return content.strip()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(e)