    def _run_latex(self):
        texcommand = mpl.rcParams["pgf.texsystem"]
        cbook._check_and_log_subprocess(
            [texcommand, "-interaction=nonstopmode", "-halt-on-error",
             os.path.basename(self._fname_tex)],
            _log, cwd=self._tmpdir)
        # copy file contents to target
        shutil.copyfile(self._fname_pdf, self._outputfile)
