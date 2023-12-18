"""
This colorizer is going to use ANSI escape codes to colorize the output. It has some colors pre-built.
Specifically:

    - Red
    - Green
    - Yellow
    - Blue
    - Magenta
    - Cyan
    - White
    - Orange
    - Purple
    - Pink
    - Grey
"""

class Colorizer:
    def __init__(self, color):
        self.color = color
        self.colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "orange": "\033[38;5;208m",
            "purple": "\033[38;5;135m",
            "pink": "\033[38;5;219m",
            "grey": "\033[38;5;246m",
            "reset": "\033[0m"
        }
        if self.color not in self.colors:
            raise Exception("Color not found")
        
    def colorize(self, text):
        return self.colors[self.color] + text + self.colors["reset"]