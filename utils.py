from inquirer import themes
from blessed import Terminal

term = Terminal()

class UITheme(themes.Theme):
    def __init__(self):
        super(UITheme, self).__init__()
        self.Question.mark_color = term.magenta
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.magenta
        self.Checkbox.selection_icon = '>'
        self.Checkbox.selected_icon = 'X'
        self.Checkbox.selected_color = term.magenta + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = 'o'
        self.List.selection_color = term.magenta
        self.List.selection_cursor = '>'
        self.List.unselected_color = term.normal