import requests
import json

class GPT:
    with open("key.txt", 'r') as F:
        KEY = F.read().strip()
        F.close()

    def GET_ANS(MSG):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = GPT.KEY
        model = "gpt-3.5-turbo"

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            ######### CONFIGURABLE #########
            temperature = 0.1
            top_p = 0.1
            ################################
            
            body = json.dumps({
                "model": model,
                "temperature": temperature,
                "top_p": top_p,
                "messages": [{"role": "user", "content": MSG}]
            })

            response = requests.post(url, headers=headers, data=body)
            response.raise_for_status()
            
            response_data = response.json()
            
            choice = response_data["choices"]
            within_choice = choice[0]
            message = within_choice["message"]
            content = message["content"]
            return content.strip()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(e)