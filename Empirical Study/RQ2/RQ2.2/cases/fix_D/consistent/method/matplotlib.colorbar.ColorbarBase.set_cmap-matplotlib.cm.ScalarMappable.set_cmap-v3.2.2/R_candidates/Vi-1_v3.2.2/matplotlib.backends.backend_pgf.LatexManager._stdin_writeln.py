    def _stdin_writeln(self, s):
        if self.latex is None:
            self._setup_latex_process()
        self.latex_stdin_utf8.write(s)
        self.latex_stdin_utf8.write("\n")
        self.latex_stdin_utf8.flush()
