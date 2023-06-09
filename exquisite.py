import json
import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import openai
from dotenv import load_dotenv

from poem import Poem


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Exquisite Corpse!")
        self.master.geometry("600x600")
        self.master.config(bg="#88769c")
        self.create_widgets()

        # fetch API key from environment
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')


        # configuration
        with open('gpt_config.json', 'r') as CONFIG:
            self.config = json.load(CONFIG)

        # system prompt
        with open('instructions.txt', 'r') as INSTRUCT:
            self.instructs = INSTRUCT.read()
        
        self.poem = Poem()
        self.first = True

    def create_widgets(self):
        # Text box
        self.textbox = tk.Text(self.master)
        self.textbox.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        # AI button
        self.ai_button = tk.Button(self.master, text="Fold", command=self.add_ai_line)
        self.ai_button.grid(row=1, column=1, sticky="sew", padx=(10, 4), pady=10)

        # Reveal poem button
        self.reveal_button = tk.Button(self.master, text="Reveal Poem", command=self.reveal_poem)
        self.reveal_button.grid(row=1, column=2, sticky="sew", padx=(0, 10), pady=10)

        # Menu
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save...", command=self.save_file)
        filemenu.add_command(label="Clear...", command=self.clear_poem)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

    def save_file(self):
        poem_text = self.poem.get_poem()
        # Open file dialog and display selected file in textbox
        files = [('Text Document', '*.txt')]
        file_path = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
        with open(file_path, 'w') as FILE:
            FILE.write(poem_text)
        self.poem.dirty = False

    def clear_poem(self):
        if self.poem.dirty:
            answer = messagebox.askyesno("Exquisite-corpse", "Would you like to save your poem?")
            if answer == True:
                self.save_file()
        self.poem.clear_poem()
        self.textbox.delete("1.0", tk.END)
        self.ai_button['state'] = tk.NORMAL
        self.first = True

    def exit_app(self):
        if self.poem.dirty:
            answer = messagebox.askyesno("Exquisite-corpse", "Would you like to save your poem?")
            if answer == True:
                self.save_file()
        self.master.quit()

    def add_ai_line(self):
        # Generate the next line of poetry using GPT-4
        user_text = self.textbox.get("1.0", "end-1c")
        self.poem.add_lines(user_text, first=self.first)
        prompt = [{'role': 'system', 'content': self.instructs}]
        self.first = False
        prompt.append(self.poem.get_prompt())

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

        text = response.choices[0].message.content.strip()
        self.poem.add_lines(text)
        self.textbox.delete("1.0",tk.END)
        self.textbox.insert("1.0", self.poem.get_last_line())

    def reveal_poem(self):
        # Show the full current poem
        self.textbox.delete("1.0",tk.END)
        self.textbox.insert("1.0", self.poem.get_poem())
        self.ai_button['state'] = tk.DISABLED
        

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
