import os
import time
import json
import requests
from dotenv import load_dotenv


class HuggingFace:
    def __init__(self, config):
        self.api_url = 'https://api-inference.huggingface.co/models/' + config['model']
        api_token = os.getenv('HF_KEY') 
        self.headers = {'Authorization': f'Bearer {api_token}'}

        self.parameters = {'max_length': config['max_length'],
                           'temperature': config['temperature']}
        self.config = config

    def query(self, sys_prompt, user_prompt):
        prompt = self.config['prompt_template'].replace('%sys_prompt%', sys_prompt)
        prompt = prompt.replace('%user_prompt%', user_prompt)
        prompt = {'parameters': self.parameters, 'inputs': prompt}
        inputs = json.dumps(prompt)

        retry = True
        count = 0
        while retry:
            response = requests.post(self.api_url,
                                    headers=self.headers,
                                    data=inputs)
            response_json = response.json()
            if response.status_code == 503:
                count += 1
                timeout = response_json['estimated_time']
                time.sleep(timeout)
                if count == 3:
                    print('Retried 3 times.')
                    break
                continue
            retry = False

        return response


def test():
    with open('hf_config.json', 'r') as FILE:
        config = json.load(FILE)
    hf = HuggingFace(config)

    sys_prompt = "You are a useful AI assistant."
    user_prompt = "Tell me about yourself"

    response = hf.query(sys_prompt, user_prompt)
    print(response.text)

if __name__ == '__main__':
    test()