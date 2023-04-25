import os
import openai
from dotenv import load_dotenv
from tkinter import messagebox


class OpenAI:
    def __init__(self, config):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_KEY')
        self.config = config

    def query(self, sys_prompt, user_prompt):
        prompt = [{'role': 'system', 'content': sys_prompt}]
        prompt.append({'role': 'user', 'content': user_prompt})

        try:
            response = openai.ChatCompletion.create(
                model=self.config['model'],
                messages=prompt,
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature'],
                top_p=self.config['top_p'],
                n=self.config['n'],
                presence_penalty=self.config['presence_penalty'],
                frequency_penalty=self.config['frequency_penalty']
            )
        except openai.error.AuthenticationError:
            messagebox.showerror('Exquisite-corpse',
                                 'You have not setup your secret key!')
            self.master.quit()
        except:
            messagebox.showerror('Exquisite-corpse',
                                 'An error has occured!')
            return
        
        return response.choices[0].message.content.strip()
