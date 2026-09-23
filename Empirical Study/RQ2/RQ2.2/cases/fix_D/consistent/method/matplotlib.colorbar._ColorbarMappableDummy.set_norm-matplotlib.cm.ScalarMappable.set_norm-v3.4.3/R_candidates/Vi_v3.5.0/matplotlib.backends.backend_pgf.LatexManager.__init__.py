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
