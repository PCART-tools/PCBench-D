    def __init__(self, message, latex_output=""):
        Exception.__init__(self, message)
        self.latex_output = latex_output
