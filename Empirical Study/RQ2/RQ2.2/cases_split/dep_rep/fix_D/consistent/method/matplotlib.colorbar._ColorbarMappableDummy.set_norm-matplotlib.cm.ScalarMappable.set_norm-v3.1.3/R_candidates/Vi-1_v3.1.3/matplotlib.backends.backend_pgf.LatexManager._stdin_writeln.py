    def _stdin_writeln(self, s):
        self.latex_stdin_utf8.write(s)
        self.latex_stdin_utf8.write("\n")
        self.latex_stdin_utf8.flush()
