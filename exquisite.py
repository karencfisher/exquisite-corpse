#! /usr/bin/env python3
# Copyright (c) 2023 karencfisher, et al.

import json, random
import os
import sys

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font

import openai
from dotenv import load_dotenv

from poem import Poem

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # state
        self.poem = Poem()
        self.ignore_first = False # ignore the first line when folding?
        self.isfolded = False # is the poem folded? then text hidden

        # options
        self.opt_textsize = 24 # textbox font size
        self.opt_unfold = True # add interim "unfolded" state to hide previous input, ie. when used within a group
        self.opt_random = True # randomly choose between ai and human when folding?
        self.opt_random_ai = 50 # percent chance to get an ai response
        self.opt_dummy_ai = True # use dummy ai text instead of the OpenAI API?
        self.opt_breaks = True # force line break between folds
        self.opt_tags = True # prepend writer tags per fold: <ai> or <human>

        # configure window
        self.master = master
        self.master.title("Exquisite Corpse!")
        self.master.geometry("600x600")
        self.master.config(bg="#88769c")
        self.create_widgets()

        # fetch API key from environment
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # load configuration and system prompt
        scriptdir = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(f"{scriptdir}/gpt_config.json", "r") as CONFIG:
            self.config = json.load(CONFIG)
        with open(f"{scriptdir}/instructions.txt", "r") as INSTRUCT:
            self.instructs = INSTRUCT.read()

    def create_widgets(self):
        """ Create window widgets: textbox & buttons. """

        # text box
        self.textbox = tk.Text(self.master, font=Font(family="TkDefaultFont", size=self.opt_textsize),
                               bg="white", highlightthickness=0)
        self.textbox.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        # fold button
        self.fold_button = tk.Button(self.master, text="Fold",
                                     command=(self.toggle_fold if self.opt_unfold else self.fold_poem))
        self.fold_button.grid(row=1, column=1, sticky="se", padx=(4, 10), pady=10)

        # reveal poem button
        self.reveal_button = tk.Button(self.master, text="Reveal Poem", command=self.reveal_poem)
        self.reveal_button.grid(row=1, column=0, sticky="sw", padx=(10, 4), pady=10)

        # menu
        modkey = "Command" if sys.platform == "darwin" else "Control"
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        if self.opt_unfold:
            filemenu.add_command(label="Un/Fold", command=self.toggle_fold, accelerator=f"{modkey}-f")
        else:
            filemenu.add_command(label="Fold", command=self.fold_poem, accelerator=f"{modkey}-f")
        filemenu.add_command(label="Reveal Poem", command=self.reveal_poem, accelerator=f"{modkey}-r")
        filemenu.add_separator()
        filemenu.add_command(label="Save...", command=self.save_poem, accelerator=f"{modkey}-S")
        filemenu.add_command(label="Clear...", command=self.clear_poem, accelerator=f"Shift-{modkey}-C")
        if sys.platform == "darwin": # override default quit on macOS
            self.master.createcommand("::tk::mac::Quit", self.exit_app)
        else: # add menu item
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=filemenu)
        viewmenu = tk.Menu(menubar, tearoff=0) # for fullscreen menu option
        menubar.add_cascade(label="View", menu=viewmenu)
        self.master.config(menu=menubar)
        self.filemenu = filemenu

        # key bindings, etc
        self.master.bind_all(f"<{modkey}-s>", self.save_poem)
        self.master.bind_all(f"<{modkey}-C>", self.clear_poem)
        self.bind_for_folding()

        self.textbox.focus_set()

    def bind_for_folding(self):
        """ Update key bindings, menu items, and buttons for folding, ie. input. """
        modkey = "Command" if sys.platform == "darwin" else "Control"
        self.master.bind_all(f"<{modkey}-f>", self.toggle_fold if self.opt_unfold else self.fold_poem)
        self.master.bind_all(f"<{modkey}-r>", self.reveal_poem)
        self.filemenu.entryconfig("Un/Fold" if self.opt_unfold else "Fold", state=tk.NORMAL)
        self.filemenu.entryconfig("Reveal Poem" if self.opt_unfold else "Fold", state=tk.NORMAL)
        self.fold_button["state"] = tk.NORMAL
        self.reveal_button.configure(text="Reveal Poem", command=self.reveal_poem)
        if self.opt_unfold: self.fold_button.configure(text="Fold")

    def bind_for_reveal(self):
        """ Update key bindings, menu items, and buttons for the poem reveal, ie. display. """
        modkey = "Command" if sys.platform == "darwin" else "Control"
        self.master.unbind(f"<{modkey}-f>")
        self.master.unbind(f"<{modkey}-r>")
        self.filemenu.entryconfig("Un/Fold" if self.opt_unfold else "Fold", state=tk.DISABLED)
        self.filemenu.entryconfig("Reveal Poem" if self.opt_unfold else "Fold", state=tk.DISABLED)
        self.fold_button["state"] = tk.DISABLED
        self.reveal_button.configure(text="Clear Poem", command=self.clear_poem)

    def save_poem(self, event=None):
        """ Open save dialog and display selected file in textbox. """
        poem_text = self.poem.get_poem()
        files = [("Text Document", "*.txt")]
        file_path = filedialog.asksaveasfilename(filetypes=files, defaultextension=files,
                                                 title="Save Poem", initialfile="poem.txt")
        self.poem.save_to(file_path)
        self.master.focus_set()

    def clear_poem(self, event=None):
        """ Clear poem and reset for next input. """
        if self.poem.dirty:
            self.ask_to_save_poem()
        self.poem.clear_poem()
        self.clear_text()
        self.ignore_first = False
        self.bind_for_folding()
        self.textbox.focus_set()

    def exit_app(self, event=None):
        """ Ask to save before quitting. """
        if self.poem.dirty:
            self.ask_to_save_poem()
        self.master.quit()

    def add_human_lines(self):
        """ Add current text lines into the poem. """
        user_text = self.get_text()
        if user_text == "":
            return False
        if self.opt_breaks: self.poem.add_break()
        if self.opt_tags: self.poem.add_lines("<human>")
        self.poem.add_lines(user_text, ignore_first=self.ignore_first)
        return True

    def add_ai_lines(self):
        """ Generate the next lines of poetry using ChatGPT. """

        # add any text entered before revealing
        if not self.add_human_lines(): return

        # add dummy ai poem text
        if self.opt_dummy_ai:
            if self.opt_breaks: self.poem.add_break()
            if self.opt_tags: self.poem.add_lines("<ai>")
            dummy = "Roses are red\n Violets blue,\nSugar is sweet\n And so are you."
            self.poem.add_lines(dummy)
            return True
        
        # send prompt for ChatGPT repsonse
        prompt = [{"role": "system", "content": self.instructs}]
        prompt.append(self.poem.get_prompt())
        try:
            response = openai.ChatCompletion.create(
                model=self.config["model"],
                messages=prompt,
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"],
                top_p=self.config["top_p"],
                n=self.config["n"],
                presence_penalty=self.config["presence_penalty"],
                frequency_penalty=self.config["frequency_penalty"]
            )
        except openai.error.AuthenticationError:
            messagebox.showerror("Exquisite-corpse",
                                 "You have not set up your OpenAI secret key!")
            self.master.quit()
        except Exception as exc:
            messagebox.showerror("Exquisite-corpse",
                                 f"An error has occured!\n{exc}")
            return False
        text = response.choices[0].message.content.strip()
        self.poem.add_lines(text)
        return True

    def toggle_fold(self, event=None):
        """
        Toggle between folded and unfolded states:
        * folded: fold current text into the poem, hide last line, disable input
        * unfolded: show last line, ready for next input
        """
        self.isfolded = not self.isfolded
        if self.isfolded:
            self.fold_poem()
            self.clear_text() # hide last line
            self.ignore_first = False
            self.fold_button.configure(text="Unfold")
            self.textbox["state"] = tk.DISABLED
            self.textbox.config(bg=self.master.cget("bg"))#"#eee")
        else:
            self.unfold_poem()
            self.fold_button.configure(text="Fold")
            self.textbox.config(bg="white")

    def fold_poem(self, event=None):
        """
        Fold current text into the poem. Leave last line visible.

        If opt_random = True, randomly chooses between human or ChatGPT for the
        next lines, otherwise always generate a ChatGPT response.
        """
        if self.opt_random:
            if(random.randint(0, 100) < self.opt_random_ai):
                if not self.add_ai_lines(): return
            else:
                if not self.add_human_lines(): return
        else:
            # ChatGPT
            if not self.add_ai_line(): return
        self.set_text(self.poem.get_last_line())
        self.ignore_first = True

    def unfold_poem(self, event=None):
        """ Unfold text to show last poem line. """
        self.textbox["state"] = tk.NORMAL
        self.set_text(self.poem.get_last_line())
        self.ignore_first = True

    def reveal_poem(self, event=None):
        """ Show the full poem. """

        # add any prev text to the poem
        self.textbox["state"] = tk.NORMAL
        self.textbox.config(bg="white")
        linecount = len(self.get_text().strip().split('\n'))
        if (self.ignore_first and linecount > 1) or \
           (not self.ignore_first and linecount > 0):
           self.add_human_lines()

        # show the poem
        self.set_text(self.poem.get_poem())
        self.bind_for_reveal()

    def get_text(self):
        """ Get current text in the text box. """
        return self.textbox.get("1.0", "end-1c")

    def clear_text(self):
        """ Clear text in the text box. """
        self.textbox.delete("1.0", tk.END)

    def set_text(self, text):
        """ Set text in the text box. """
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", text)

    def ask_to_save_poem(self):
        """ Open a dialog asking to save poem. If yes, then open save dialog. """
        if messagebox.askyesno("Exquisite-corpse",
                               "Would you like to save your poem?"):
            self.save_poem()
        else:
            self.master.focus_set()

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
