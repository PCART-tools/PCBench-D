    def __init__(self):
        # store references for __del__
        self._os_path = os.path
        self._shutil = shutil

        # create a tmp directory for running latex, remember to cleanup
        self.tmpdir = tempfile.mkdtemp(prefix="mpl_pgf_lm_")
        LatexManager._unclean_instances.add(self)

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
                             "or error in preamble:\n%s" % stdout)

        self.latex = None  # Will be set up on first use.
        self.str_cache = {}  # cache for strings already processed
