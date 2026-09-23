    def _setup_latex_process(self):
        # open LaTeX process for real work
        self.latex = subprocess.Popen(
            [self.texcommand, "-halt-on-error"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            encoding="utf-8", cwd=self.tmpdir)
        # write header with 'pgf_backend_query_start' token
        self._stdin_writeln(self._build_latex_header())
        # read all lines until our 'pgf_backend_query_start' token appears
        self._expect("*pgf_backend_query_start")
        self._expect_prompt()
