    def _setup_latex_process(self, *, expect_reply=True):
        # Open LaTeX process for real work; register it for deletion.  On
        # Windows, we must ensure that the subprocess has quit before being
        # able to delete the tmpdir in which it runs; in order to do so, we
        # must first `kill()` it, and then `communicate()` with it.
        try:
            self.latex = subprocess.Popen(
                [mpl.rcParams["pgf.texsystem"], "-halt-on-error"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                encoding="utf-8", cwd=self.tmpdir)
        except FileNotFoundError as err:
            raise RuntimeError(
                f"{mpl.rcParams['pgf.texsystem']!r} not found; install it or change "
                f"rcParams['pgf.texsystem'] to an available TeX implementation"
            ) from err
        except OSError as err:
            raise RuntimeError(
                f"Error starting {mpl.rcParams['pgf.texsystem']!r}") from err

        def finalize_latex(latex):
            latex.kill()
            latex.communicate()

        self._finalize_latex = weakref.finalize(
            self, finalize_latex, self.latex)
        # write header with 'pgf_backend_query_start' token
        self._stdin_writeln(self._build_latex_header())
        if expect_reply:  # read until 'pgf_backend_query_start' token appears
            self._expect("*pgf_backend_query_start")
            self._expect_prompt()
