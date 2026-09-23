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
        self.str_cache = {}  # cache for strings already processed

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

    @_api.deprecated("3.3")
    def latex_stdin_utf8(self):
        return self.latex.stdin

    def get_width_height_descent(self, text, prop):
        """
        Get the width, total height and descent for a text typeset by the
        current LaTeX environment.
        """

        # apply font properties and define textbox
        prop_cmds = _font_properties_str(prop)
        textbox = "\\sbox0{%s %s}" % (prop_cmds, text)

        # check cache
        if textbox in self.str_cache:
            return self.str_cache[textbox]

        # send textbox to LaTeX and wait for prompt
        self._stdin_writeln(textbox)
        try:
            self._expect_prompt()
        except LatexError as e:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, e.latex_output)) from e

        # typeout width, height and text offset of the last textbox
        self._stdin_writeln(r"\typeout{\the\wd0,\the\ht0,\the\dp0}")
        # read answer from latex and advance to the next prompt
        try:
            answer = self._expect_prompt()
        except LatexError as e:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, e.latex_output)) from e

        # parse metrics from the answer string
        try:
            width, height, offset = answer.splitlines()[0].split(",")
        except Exception as err:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, answer)) from err
        w, h, o = float(width[:-2]), float(height[:-2]), float(offset[:-2])

        # the height returned from LaTeX goes from base to top.
        # the height matplotlib expects goes from bottom to top.
        self.str_cache[textbox] = (w, h + o, o)
        return w, h + o, o
