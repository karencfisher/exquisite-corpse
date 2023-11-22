# copyright (c) 2023 karencfisher, et al.
# updated by Dan Wilcox <dan.wilcox@zkm.de> ZKM | Hertz-Lab 2023

import sys

class Poem:
    """ A sequence of string text lines. """

    def __init__(self):
        self.dirty = False # has the poem changed since the last save?
        self.complete_text = [] # complete poem as an array of separate lines

    def get_last_line(self, max_words=50):
        """
        Returns the last line of the poem, up to max_words in length.

        Set max_words=0 to return full line.
        """
        if len(self.complete_text) == 0: return ""
        last_line = self.complete_text[-1]
        if max_words < 1: return ""
        return " ".join(last_line.split(" ")[-max_words:])
    
    def get_prompt(self):
        """ Returns a prompt with the last line of the poem for ChatGPT. """
        if len(self.complete_text) == 0:
            self.complete_text.append('\n')
        last_line = self.complete_text[-1]
        prompt = {"role": "user", "content": last_line}
        return prompt
    
    def get_poem(self):
        """ Returns the complete poem as a string. """
        return "".join(self.complete_text).lstrip()
    
    def clear_poem(self):
        """ Clears the poem. """
        self.complete_text = []
        self.dirty = False
    
    def add_lines(self, text, ignore_first=False):
        """
        Add endline-separated lines in string text to the poem.

        Set ignore_first=True to ignore first line.
        """
        lines = text.strip().split('\n')
        start = 1 if ignore_first else 0
        for line in lines[start:]:
            self.complete_text.append(line + '\n')
        self.dirty = True

    def add_break(self):
        """ Add a line break to the poem text. """
        self.complete_text.append('\n')

    def save_to(self, file_path, mode="w"):
        """
            Save the poem as a string to a text file at file_path.
            Returns True on success.
        """
        try:
            with open(file_path, mode) as FILE:
                FILE.write(self.get_poem())
        except Exception as exc:
            print(exc, file=sys.stderr)
            return False
        self.dirty = False
        return True
