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

        self.latex = None  # Will be set up on first use.
        self.str_cache = {}  # cache for strings already processed
