import os
import json
import torch
from dotenv import load_dotenv
from transformers import (AutoTokenizer, AutoModelForCausalLM, 
                          StoppingCriteria, StoppingCriteriaList)


class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [50278, 50279, 50277, 1, 0]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False
    

class HuggingFace:
    def __init__(self, config):
        model = config['model']
        print(f'Loading {model}...')
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(model)
        print('Model loaded.')
        self.config = config

    def query(self, sys_prompt, user_prompt):
        prompt = self.config['prompt_template'].replace('%sys_prompt%', sys_prompt)
        prompt = prompt.replace('%user_prompt%', user_prompt)

        inputs = self.tokenizer(prompt, return_tensors='pt').to("cpu")
        tokens = self.model.generate(
            **inputs,
            max_new_tokens=self.config['max_length'],
            temperature=self.config['temperature'],
            do_sample=True,
            stopping_criteria=StoppingCriteriaList([StopOnTokens()])
        )
        return(self.tokenizer.decode(tokens[0], skip_special_tokens=True))

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