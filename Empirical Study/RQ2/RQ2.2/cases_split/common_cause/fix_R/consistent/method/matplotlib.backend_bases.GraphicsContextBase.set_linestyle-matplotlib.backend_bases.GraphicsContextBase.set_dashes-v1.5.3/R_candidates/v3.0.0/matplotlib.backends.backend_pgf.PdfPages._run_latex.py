    def _run_latex(self):
        texcommand = rcParams["pgf.texsystem"]
        cmdargs = [
            texcommand,
            "-interaction=nonstopmode",
            "-halt-on-error",
            os.path.basename(self._fname_tex),
        ]
        try:
            subprocess.check_output(
                cmdargs, stderr=subprocess.STDOUT, cwd=self._tmpdir
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                "%s was not able to process your file.\n\nFull log:\n%s"
                % (texcommand, e.output.decode('utf-8')))

        # copy file contents to target
        shutil.copyfile(self._fname_pdf, self._outputfile)
