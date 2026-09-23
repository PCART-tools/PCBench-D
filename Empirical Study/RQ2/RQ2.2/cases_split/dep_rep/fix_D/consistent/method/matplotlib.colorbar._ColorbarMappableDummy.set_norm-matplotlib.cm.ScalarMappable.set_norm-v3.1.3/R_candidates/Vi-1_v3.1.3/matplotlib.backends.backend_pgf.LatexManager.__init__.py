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
