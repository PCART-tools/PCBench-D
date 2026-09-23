    def _setup_latex_process(self):
        # Open LaTeX process for real work; register it for deletion.  On
        # Windows, we must ensure that the subprocess has quit before being
        # able to delete the tmpdir in which it runs; in order to do so, we
        # must first `kill()` it, and then `communicate()` with it.
        self.latex = subprocess.Popen(
            [self.texcommand, "-halt-on-error"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            encoding="utf-8", cwd=self.tmpdir)

        def finalize_latex(latex):
            latex.kill()
            latex.communicate()

        self._finalize_latex = weakref.finalize(
            self, finalize_latex, self.latex)
        # write header with 'pgf_backend_query_start' token
        self._stdin_writeln(self._build_latex_header())
        # read all lines until our 'pgf_backend_query_start' token appears
        self._expect("*pgf_backend_query_start")
        self._expect_prompt()
