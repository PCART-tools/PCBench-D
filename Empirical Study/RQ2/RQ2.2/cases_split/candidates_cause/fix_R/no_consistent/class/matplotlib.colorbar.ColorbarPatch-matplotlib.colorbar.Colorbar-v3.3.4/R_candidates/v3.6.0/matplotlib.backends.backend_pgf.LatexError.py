class LatexError(Exception):
    def __init__(self, message, latex_output=""):
        super().__init__(message)
        self.latex_output = latex_output

    def __str__(self):
        s, = self.args
        if self.latex_output:
            s += "\n" + self.latex_output
        return s
