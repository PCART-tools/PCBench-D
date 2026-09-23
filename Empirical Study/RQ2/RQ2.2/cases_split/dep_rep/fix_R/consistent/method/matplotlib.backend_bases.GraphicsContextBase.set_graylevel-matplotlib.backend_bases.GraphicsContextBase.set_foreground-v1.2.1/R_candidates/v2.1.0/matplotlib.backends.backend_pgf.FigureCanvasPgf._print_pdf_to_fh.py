    def _print_pdf_to_fh(self, fh, *args, **kwargs):
        w, h = self.figure.get_figwidth(), self.figure.get_figheight()

        try:
            # create temporary directory for compiling the figure
            tmpdir = tempfile.mkdtemp(prefix="mpl_pgf_")
            fname_pgf = os.path.join(tmpdir, "figure.pgf")
            fname_tex = os.path.join(tmpdir, "figure.tex")
            fname_pdf = os.path.join(tmpdir, "figure.pdf")

            # print figure to pgf and compile it with latex
            self.print_pgf(fname_pgf, *args, **kwargs)

            latex_preamble = get_preamble()
            latex_fontspec = get_fontspec()
            latexcode = """
\\documentclass[12pt]{minimal}
\\usepackage[paperwidth=%fin, paperheight=%fin, margin=0in]{geometry}
%s
%s
\\usepackage{pgf}

\\begin{document}
\\centering
\\input{figure.pgf}
\\end{document}""" % (w, h, latex_preamble, latex_fontspec)
            with codecs.open(fname_tex, "w", "utf-8") as fh_tex:
                fh_tex.write(latexcode)

            texcommand = get_texcommand()
            cmdargs = [str(texcommand), "-interaction=nonstopmode",
                       "-halt-on-error", "figure.tex"]
            try:
                check_output(cmdargs, stderr=subprocess.STDOUT, cwd=tmpdir)
            except subprocess.CalledProcessError as e:
                raise RuntimeError("%s was not able to process your file.\n\nFull log:\n%s" % (texcommand, e.output))

            # copy file contents to target
            with open(fname_pdf, "rb") as fh_src:
                shutil.copyfileobj(fh_src, fh)
        finally:
            try:
                shutil.rmtree(tmpdir)
            except:
                TmpDirCleaner.add(tmpdir)
