class LatexManager:
    """
    The LatexManager opens an instance of the LaTeX application for
    determining the metrics of text elements. The LaTeX environment can be
    modified by setting fonts and/or a custem preamble in the rc parameters.
    """
    _unclean_instances = weakref.WeakSet()

    @staticmethod
    def _build_latex_header():
        latex_preamble = get_preamble()
        latex_fontspec = get_fontspec()
        # Create LaTeX header with some content, else LaTeX will load some math
        # fonts later when we don't expect the additional output on stdout.
        # TODO: is this sufficient?
        latex_header = [r"\documentclass{minimal}",
                        latex_preamble,
                        latex_fontspec,
                        r"\begin{document}",
                        r"text $math \mu$",  # force latex to load fonts now
                        r"\typeout{pgf_backend_query_start}"]
        return "\n".join(latex_header)

    @staticmethod
    def _cleanup_remaining_instances():
        unclean_instances = list(LatexManager._unclean_instances)
        for latex_manager in unclean_instances:
            latex_manager._cleanup()

    def _stdin_writeln(self, s):
        self.latex_stdin_utf8.write(s)
        self.latex_stdin_utf8.write("\n")
        self.latex_stdin_utf8.flush()

    def _expect(self, s):
        exp = s.encode("utf8")
        buf = bytearray()
        while True:
            b = self.latex.stdout.read(1)
            buf += b
            if buf[-len(exp):] == exp:
                break
            if not len(b):
                raise LatexError("LaTeX process halted", buf.decode("utf8"))
        return buf.decode("utf8")

    def _expect_prompt(self):
        return self._expect("\n*")

    def __init__(self):
        # store references for __del__
        self._os_path = os.path
        self._shutil = shutil

        # create a tmp directory for running latex, remember to cleanup
        self.tmpdir = tempfile.mkdtemp(prefix="mpl_pgf_lm_")
        LatexManager._unclean_instances.add(self)

        # test the LaTeX setup to ensure a clean startup of the subprocess
        self.texcommand = rcParams["pgf.texsystem"]
        self.latex_header = LatexManager._build_latex_header()
        latex_end = "\n\\makeatletter\n\\@@end\n"
        try:
            latex = subprocess.Popen([self.texcommand, "-halt-on-error"],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     cwd=self.tmpdir)
        except FileNotFoundError:
            raise RuntimeError(
                "Latex command not found. Install %r or change "
                "pgf.texsystem to the desired command." % self.texcommand)
        except OSError:
            raise RuntimeError("Error starting process %r" % self.texcommand)
        test_input = self.latex_header + latex_end
        stdout, stderr = latex.communicate(test_input.encode("utf-8"))
        if latex.returncode != 0:
            raise LatexError("LaTeX returned an error, probably missing font "
                             "or error in preamble:\n%s" % stdout)

        # open LaTeX process for real work
        latex = subprocess.Popen([self.texcommand, "-halt-on-error"],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 cwd=self.tmpdir)
        self.latex = latex
        self.latex_stdin_utf8 = codecs.getwriter("utf8")(self.latex.stdin)
        # write header with 'pgf_backend_query_start' token
        self._stdin_writeln(self._build_latex_header())
        # read all lines until our 'pgf_backend_query_start' token appears
        self._expect("*pgf_backend_query_start")
        self._expect_prompt()

        # cache for strings already processed
        self.str_cache = {}

    def _cleanup(self):
        if not self._os_path.isdir(self.tmpdir):
            return
        try:
            self.latex.communicate()
            self.latex_stdin_utf8.close()
            self.latex.stdout.close()
        except Exception:
            pass
        try:
            self._shutil.rmtree(self.tmpdir)
            LatexManager._unclean_instances.discard(self)
        except Exception:
            sys.stderr.write("error deleting tmp directory %s\n" % self.tmpdir)

    def __del__(self):
        _log.debug("deleting LatexManager")
        self._cleanup()

    def get_width_height_descent(self, text, prop):
        """
        Get the width, total height and descent for a text typesetted by the
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
                             .format(text, e.latex_output))

        # typeout width, height and text offset of the last textbox
        self._stdin_writeln(r"\typeout{\the\wd0,\the\ht0,\the\dp0}")
        # read answer from latex and advance to the next prompt
        try:
            answer = self._expect_prompt()
        except LatexError as e:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, e.latex_output))

        # parse metrics from the answer string
        try:
            width, height, offset = answer.splitlines()[0].split(",")
        except:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, answer))
        w, h, o = float(width[:-2]), float(height[:-2]), float(offset[:-2])

        # the height returned from LaTeX goes from base to top.
        # the height matplotlib expects goes from bottom to top.
        self.str_cache[textbox] = (w, h + o, o)
        return w, h + o, o
