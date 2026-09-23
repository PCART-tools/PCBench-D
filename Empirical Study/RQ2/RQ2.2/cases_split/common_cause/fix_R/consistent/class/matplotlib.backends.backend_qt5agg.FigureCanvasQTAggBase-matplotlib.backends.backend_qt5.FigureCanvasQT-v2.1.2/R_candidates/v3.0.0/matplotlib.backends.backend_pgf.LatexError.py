class LatexError(Exception):
    def __init__(self, message, latex_output=""):
        super().__init__(message)
        self.latex_output = latex_output
