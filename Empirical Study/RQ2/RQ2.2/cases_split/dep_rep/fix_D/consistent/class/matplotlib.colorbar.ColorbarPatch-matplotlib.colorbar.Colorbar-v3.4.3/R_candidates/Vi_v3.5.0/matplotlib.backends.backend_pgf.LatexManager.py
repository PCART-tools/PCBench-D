class LatexManager:
    """
    The LatexManager opens an instance of the LaTeX application for
    determining the metrics of text elements. The LaTeX environment can be
    modified by setting fonts and/or a custom preamble in `.rcParams`.
    """

    @staticmethod
    def _build_latex_header():
        latex_preamble = get_preamble()
        latex_fontspec = get_fontspec()
        # Create LaTeX header with some content, else LaTeX will load some math
        # fonts later when we don't expect the additional output on stdout.
        # TODO: is this sufficient?
        latex_header = [
            r"\documentclass{minimal}",
            # Include TeX program name as a comment for cache invalidation.
            # TeX does not allow this to be the first line.
            rf"% !TeX program = {mpl.rcParams['pgf.texsystem']}",
            # Test whether \includegraphics supports interpolate option.
            r"\usepackage{graphicx}",
            latex_preamble,
            latex_fontspec,
            r"\begin{document}",
            r"text $math \mu$",  # force latex to load fonts now
            r"\typeout{pgf_backend_query_start}",
        ]
        return "\n".join(latex_header)

    @classmethod
    def _get_cached_or_new(cls):
        """
        Return the previous LatexManager if the header and tex system did not
        change, or a new instance otherwise.
        """
        return cls._get_cached_or_new_impl(cls._build_latex_header())

    @classmethod
    @functools.lru_cache(1)
    def _get_cached_or_new_impl(cls, header):  # Helper for _get_cached_or_new.
        return cls()

    def _stdin_writeln(self, s):
        if self.latex is None:
            self._setup_latex_process()
        self.latex.stdin.write(s)
        self.latex.stdin.write("\n")
        self.latex.stdin.flush()

    def _expect(self, s):
        s = list(s)
        chars = []
        while True:
            c = self.latex.stdout.read(1)
            chars.append(c)
            if chars[-len(s):] == s:
                break
            if not c:
                self.latex.kill()
                self.latex = None
                raise LatexError("LaTeX process halted", "".join(chars))
        return "".join(chars)

    def _expect_prompt(self):
        return self._expect("\n*")

    def __init__(self):
        # create a tmp directory for running latex, register it for deletion
        self._tmpdir = TemporaryDirectory()
        self.tmpdir = self._tmpdir.name
        self._finalize_tmpdir = weakref.finalize(self, self._tmpdir.cleanup)

        # test the LaTeX setup to ensure a clean startup of the subprocess
        self.texcommand = mpl.rcParams["pgf.texsystem"]
        self.latex_header = LatexManager._build_latex_header()
        latex_end = "\n\\makeatletter\n\\@@end\n"
        try:
            latex = subprocess.Popen(
                [self.texcommand, "-halt-on-error"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                encoding="utf-8", cwd=self.tmpdir)
        except FileNotFoundError as err:
            raise RuntimeError(
                f"{self.texcommand} not found.  Install it or change "
                f"rcParams['pgf.texsystem'] to an available TeX "
                f"implementation.") from err
        except OSError as err:
            raise RuntimeError("Error starting process %r" %
                               self.texcommand) from err
        test_input = self.latex_header + latex_end
        stdout, stderr = latex.communicate(test_input)
        if latex.returncode != 0:
            raise LatexError("LaTeX returned an error, probably missing font "
                             "or error in preamble.", stdout)

        self.latex = None  # Will be set up on first use.
        # Per-instance cache.
        self._get_box_metrics = functools.lru_cache()(self._get_box_metrics)

    str_cache = _api.deprecated("3.5")(property(lambda self: {}))

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

    def get_width_height_descent(self, text, prop):
        """
        Get the width, total height, and descent (in TeX points) for a text
        typeset by the current LaTeX environment.
        """
        return self._get_box_metrics(_escape_and_apply_props(text, prop))

    def _get_box_metrics(self, tex):
        """
        Get the width, total height and descent (in TeX points) for a TeX
        command's output in the current LaTeX environment.
        """
        # This method gets wrapped in __init__ for per-instance caching.
        self._stdin_writeln(  # Send textbox to TeX & request metrics typeout.
            r"\sbox0{%s}\typeout{\the\wd0,\the\ht0,\the\dp0}" % tex)
        try:
            answer = self._expect_prompt()
        except LatexError as err:
            raise ValueError("Error measuring {!r}\nLaTeX Output:\n{}"
                             .format(tex, err.latex_output)) from err
        try:
            # Parse metrics from the answer string.  Last line is prompt, and
            # next-to-last-line is blank line from \typeout.
            width, height, offset = answer.splitlines()[-3].split(",")
        except Exception as err:
            raise ValueError("Error measuring {!r}\nLaTeX Output:\n{}"
                             .format(tex, answer)) from err
        w, h, o = float(width[:-2]), float(height[:-2]), float(offset[:-2])
        # The height returned from LaTeX goes from base to top;
        # the height Matplotlib expects goes from bottom to top.
        return w, h + o, o
