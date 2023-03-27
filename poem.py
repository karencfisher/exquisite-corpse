class Poem:
    def __init__(self, lines_shown=1):
        self.dirty=False
        self.complete_text = []
        self.lines_shown = lines_shown

    def get_last_line(self):
        return self.complete_text[-1]
    
    def get_prompt(self):
        if len(self.complete_text) == 0:
            self.complete_text.append('\n')
        last_line = self.complete_text[-1]
        prompt = {'role': 'user', 'content': last_line}
        return prompt
    
    def get_poem(self):
        return ''.join(self.complete_text).lstrip()
    
    def clear_poem(self):
        self.complete_text = []
        self.dirty = False
    
    def add_lines(self, text, first=False):
        lines = text.strip().split('\n')
        start = 0 if first else self.lines_shown
        for line in lines[start:]:
            self.complete_text.append(line + '\n')
        self.dirty = True