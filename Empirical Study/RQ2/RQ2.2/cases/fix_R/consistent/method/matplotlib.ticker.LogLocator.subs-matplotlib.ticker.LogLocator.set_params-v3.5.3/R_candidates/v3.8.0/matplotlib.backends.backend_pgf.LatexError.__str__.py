    def __str__(self):
        s, = self.args
        if self.latex_output:
            s += "\n" + self.latex_output
        return s
