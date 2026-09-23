    def _print_pdf_to_fh(self, fh, *args, metadata=None, **kwargs):
        w, h = self.figure.get_figwidth(), self.figure.get_figheight()

        info_dict = _create_pdf_info_dict('pgf', metadata or {})
        hyperref_options = ','.join(
            _metadata_to_str(k, v) for k, v in info_dict.items())

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
\\PassOptionsToPackage{pdfinfo={%s}}{hyperref}
\\RequirePackage{hyperref}
\\documentclass[12pt]{minimal}
\\usepackage[paperwidth=%fin, paperheight=%fin, margin=0in]{geometry}
%s
%s
\\usepackage{pgf}

\\begin{document}
\\centering
\\input{figure.pgf}
\\end{document}""" % (hyperref_options, w, h, latex_preamble, latex_fontspec)
            pathlib.Path(fname_tex).write_text(latexcode, encoding="utf-8")

            texcommand = mpl.rcParams["pgf.texsystem"]
            cbook._check_and_log_subprocess(
                [texcommand, "-interaction=nonstopmode", "-halt-on-error",
                 "figure.tex"], _log, cwd=tmpdir)

            # copy file contents to target
            with open(fname_pdf, "rb") as fh_src:
                shutil.copyfileobj(fh_src, fh)
        finally:
            try:
                shutil.rmtree(tmpdir)
            except:
                TmpDirCleaner.add(tmpdir)
