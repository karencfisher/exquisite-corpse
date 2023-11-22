#! /usr/bin/env python3
# copyright (c) 2023 karencfisher, et al.
# updated by Dan Wilcox <dan.wilcox@zkm.de> ZKM | Hertz-Lab 2023

import json, random
import os
import sys
import argparse

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font

import openai
from dotenv import load_dotenv

# load optional translations in locale dir
try:
    import gettext
    scriptdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    gettext.bindtextdomain("base", f"{scriptdir}/locale")
    gettext.textdomain("base")
    _ = gettext.gettext
except:
    _ = lambda s: s

from poem import Poem

##### parser

def create_parser():
    """ Create commandline argyment parser. """
    parser = argparse.ArgumentParser(description="Exquisite Corpse, according to ChatGPT")
    parser.add_argument(
        "instructfile", type=str, nargs="?", metavar="INSTRUCT",
        default=None, help="custom ChatGPT instructions txt file")
    parser.add_argument(
        "--config", action="store", dest="configfile",
        default=None, help="custom ChatGPT configuration json file")
    parser.add_argument(
        "--fontsize", action="store", dest="fontsize",
        default=12, type=int, help="textbox font size in points, default: 12")
    parser.add_argument("-u", "--unfold", action="store_true", dest="unfold",
        help="enable interim \"unfolded\" state to hide previous input, ie. when used within a group")
    parser.add_argument("-r", "--random", action="store_true", dest="random",
        help="randomly choose between ai and human when folding")
    parser.add_argument(
        "--randomai", action="store", dest="random_ai",
        default=50, type=int, help="percent chance to get an ai response 0-100, default: 50")
    parser.add_argument("-d", "--dummyai", action="store_true", dest="dummy_ai",
        help="use dummy ai text instead of ChatGPT (saves money when testing)")
    parser.add_argument("-b", "--breaks", action="store_true", dest="breaks",
        help="force line breaks between folds")
    parser.add_argument("-t", "--tags", action="store_true", dest="tags",
        help="prepend writer tag lines per fold: <ai> or <human>, adds Reveal Writers menu item")
    parser.add_argument(
        "--maxwords", action="store", dest="max_words",
        default=30, type=int, help="max allowed words for prev line, useful for story text which may not use line breaks, default: 0 (allow all)")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
        help="enable verbose printing")
    return parser

##### Application

class Application(tk.Frame):
    def __init__(self, master=None, args=None):
        super().__init__(master)  

        # state
        self.poem = Poem()
        self.ignore_first = False # ignore the first line when folding?
        self.isfolded = False # is the poem folded? then text hidden

        # runtime options
        self.args = args

        # configure window
        self.master = master
        self.master.title(_("Exquisite Corpse!"))
        self.master.geometry("600x600")
        self.master.config(bg="#88769c")
        self.create_widgets()

        # fetch API key from environment
        load_dotenv()
        openai.api_key = os.getenv("SECRET_KEY")

        # load configuration
        scriptdir = os.path.dirname(os.path.realpath(sys.argv[0]))
        configfile = f"{scriptdir}/gpt_config.json" # default
        if args.configfile: configfile = args.configfile
        if self.args.verbose: print(f"config: {configfile}")
        with open(configfile, "r") as CONFIG:
            self.config = json.load(CONFIG)

        # load system prompt
        instructfile = f"{scriptdir}/instructions.txt" # default
        if args.instructfile: instructfile = args.instructfile
        if self.args.verbose: print(f"instructions: {instructfile}")
        with open(instructfile, "r") as INSTRUCT:
            self.instructs = INSTRUCT.read()

        # options summary
        if self.args.verbose:
            print(f"unfold: {args.unfold}")
            print(f"random: {args.random}")
            print(f"random ai %: {args.random_ai}")
            print(f"dummy ai: {args.dummy_ai}")
            print(f"line breaks: {args.breaks}")
            print(f"writer tags: {args.tags}")

    def create_widgets(self):
        """ Create window widgets: textbox & buttons. """

        # text box
        self.textbox = tk.Text(self.master, font=Font(family="TkDefaultFont", size=self.args.fontsize),
                               bg="white", highlightthickness=0)
        self.textbox.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        # fold button
        self.fold_button = tk.Button(self.master, text=_("Fold"),
                                     command=(self.toggle_fold if self.args.unfold else self.fold_poem))
        self.fold_button.grid(row=1, column=1, sticky="se", padx=(4, 10), pady=10)

        # reveal poem button
        self.reveal_button = tk.Button(self.master, text=_("Reveal Text"), command=self.reveal_poem)
        self.reveal_button.grid(row=1, column=0, sticky="sw", padx=(10, 4), pady=10)

        # menu
        modkey = "Command" if sys.platform == "darwin" else "Control"
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        if self.args.unfold:
            filemenu.add_command(label=_("Un/Fold"), command=self.toggle_fold, accelerator=f"{modkey}-f")
        else:
            filemenu.add_command(label=_("Fold"), command=self.fold_poem, accelerator=f"{modkey}-f")
        filemenu.add_command(label=_("Reveal Text"), command=self.reveal_poem, accelerator=f"{modkey}-r")
        if self.args.tags:
            filemenu.add_command(label=_("Reveal Writers"), command=self.reveal_writers, accelerator=f"Shift-{modkey}-r")
        filemenu.add_separator()
        filemenu.add_command(label=_("Save..."), command=self.save_poem, accelerator=f"{modkey}-S")
        filemenu.add_command(label=_("Clear..."), command=self.clear_poem, accelerator=f"Shift-{modkey}-C")
        if sys.platform == "darwin": # override default quit on macOS
            self.master.createcommand("::tk::mac::Quit", self.exit_app)
        else: # add menu item
            filemenu.add_separator()
            filemenu.add_command(label=_("Exit"), command=self.exit_app)
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
        self.master.bind_all(f"<{modkey}-f>", self.toggle_fold if self.args.unfold else self.fold_poem)
        self.master.bind_all(f"<{modkey}-r>", self.reveal_poem)
        self.filemenu.entryconfig(_("Un/Fold") if self.args.unfold else _("Fold"), state=tk.NORMAL)
        self.filemenu.entryconfig(_("Reveal Text"), state=tk.NORMAL)
        self.fold_button["state"] = tk.NORMAL
        self.reveal_button.configure(text=_("Reveal Text"), command=self.reveal_poem)
        if self.args.unfold:
            self.fold_button.configure(text=_("Fold"))
        if self.args.tags:
            self.master.unbind(f"<{modkey}-R>")
            self.filemenu.entryconfig(_("Reveal Writers"), state=tk.DISABLED)

    def bind_for_reveal(self):
        """ Update key bindings, menu items, and buttons for the poem reveal, ie. display. """
        modkey = "Command" if sys.platform == "darwin" else "Control"
        self.master.unbind(f"<{modkey}-f>")
        self.master.unbind(f"<{modkey}-r>")
        self.filemenu.entryconfig(_("Un/Fold") if self.args.unfold else _("Fold"), state=tk.DISABLED)
        self.filemenu.entryconfig(_("Reveal Text"), state=tk.DISABLED)
        self.fold_button["state"] = tk.DISABLED
        self.reveal_button.configure(text=_("Clear Text"), command=self.clear_poem)
        if self.args.tags:
            self.master.bind_all(f"<{modkey}-R>", self.reveal_writers)
            self.filemenu.entryconfig(_("Reveal Writers"), state=tk.NORMAL)

    def save_poem(self, event=None):
        """ Open save dialog and display selected file in textbox. """
        poem_text = self.poem.get_poem()
        files = [("Text Document", "*.txt")]
        file_path = filedialog.asksaveasfilename(filetypes=files, defaultextension=files,
                                                 title=_("Save Text"), initialfile="poem.txt")
        if self.args.verbose: print(f"saving to {file_path}")
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
        if self.args.verbose: print("cleared")

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
        if self.args.breaks: self.poem.add_break()
        if self.args.tags: self.poem.add_lines("<human>")
        self.poem.add_lines(user_text, ignore_first=self.ignore_first)
        if self.args.verbose: print(f"\nadd human:\n{user_text}")
        return True

    def add_ai_lines(self):
        """ Generate the next lines of poetry using ChatGPT. """

        # add any text entered before revealing
        if not self.add_human_lines(): return

        # add dummy ai poem text
        if self.args.dummy_ai:
            if self.args.breaks: self.poem.add_break()
            if self.args.tags: self.poem.add_lines("<ai>")
            dummy = "Roses are red\n Violets blue,\nSugar is sweet\n And so are you."
            self.poem.add_lines(dummy)
            if self.args.verbose: print(f"\nadd dummy ai:\n{dummy}")
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
        except openai.error.AuthenticationError as exc:
            print(f"open ai authentication failed: {exc}", file=sys.stderr)
            messagebox.showerror("Exquisite-corpse",
                                 _("OpenAI authentication failed!\nIs the secret key set and valid?"))
            self.master.quit()
            return False
        except Exception as exc:
            print(f"open ai error: {exc}", file=sys.stderr)
            messagebox.showerror("Exquisite-corpse",
                                 _("An error has occured!") +
                                 f"\n\n{exc.error.message if exc.error else exec}")
            return False
        if self.args.breaks: self.poem.add_break()
        if self.args.tags: self.poem.add_lines("<ai>")
        text = response.choices[0].message.content.strip()
        self.poem.add_lines(text)
        if self.args.verbose: print(f"\nadd ai: {text}")
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
            self.fold_button.configure(text=_("Unfold"))
            self.textbox["state"] = tk.DISABLED
            self.textbox.config(bg=self.master.cget("bg"))#"#eee")
        else:
            self.unfold_poem()
            self.fold_button.configure(text=_("Fold"))
            self.textbox.config(bg="white")

    def fold_poem(self, event=None):
        """
        Fold current text into the poem. Leave last line visible.

        If opt_random = True, randomly chooses between human or ChatGPT for the
        next lines, otherwise always generate a ChatGPT response.
        """
        if self.args.random:
            if(random.randint(0, 100) < self.args.random_ai):
                if not self.add_ai_lines(): return
            else:
                if not self.add_human_lines(): return
        else:
            # ChatGPT
            if not self.add_ai_lines(): return
        self.set_text(self.poem.get_last_line(max_words=self.args.max_words))
        self.ignore_first = True

    def unfold_poem(self, event=None):
        """ Unfold text to show last poem line. """
        self.textbox["state"] = tk.NORMAL
        self.set_text(self.poem.get_last_line(max_words=self.args.max_words))
        self.ignore_first = True

    def reveal_poem(self, event=None):
        """ Show the full poem. Strips writer tags if self.args.tags is True. """

        # add any prev text to the poem
        self.textbox["state"] = tk.NORMAL
        self.textbox.config(bg="white")
        linecount = len(self.get_text().strip().split('\n'))
        if (self.ignore_first and linecount > 1) or \
           (not self.ignore_first and linecount > 0):
           self.add_human_lines()

        # show the poem
        text = self.poem.get_poem()
        if self.args.tags:
            for t in ["<human>\n", "<ai>\n"]:
                text = text.replace(t, "")
        self.set_text(text)
        self.bind_for_reveal()

    def reveal_writers(self, event=None):
        """ Show the full poem without stripping writer tags. """
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
                               _("Would you like to save your text?")):
            self.save_poem()
        else:
            self.master.focus_set()

def main():

    # parse commandline
    parser = create_parser()
    args = parser.parse_args()

    # run application
    root = tk.Tk()
    app = Application(master=root, args=args)
    app.mainloop()

if __name__ == "__main__":
    main()
