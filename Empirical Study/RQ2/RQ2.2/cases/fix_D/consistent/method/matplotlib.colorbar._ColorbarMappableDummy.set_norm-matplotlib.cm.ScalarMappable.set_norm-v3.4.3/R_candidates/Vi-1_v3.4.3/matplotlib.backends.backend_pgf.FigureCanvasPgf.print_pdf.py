    def print_pdf(self, fname_or_fh, *args, metadata=None, **kwargs):
        """Use LaTeX to compile a pgf generated figure to pdf."""
        w, h = self.figure.get_figwidth(), self.figure.get_figheight()

        info_dict = _create_pdf_info_dict('pgf', metadata or {})
        hyperref_options = ','.join(
            _metadata_to_str(k, v) for k, v in info_dict.items())

        with TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)

            # print figure to pgf and compile it with latex
            self.print_pgf(tmppath / "figure.pgf", *args, **kwargs)

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
\\end{document}""" % (hyperref_options, w, h, get_preamble(), get_fontspec())
            (tmppath / "figure.tex").write_text(latexcode, encoding="utf-8")

            texcommand = mpl.rcParams["pgf.texsystem"]
            cbook._check_and_log_subprocess(
                [texcommand, "-interaction=nonstopmode", "-halt-on-error",
                 "figure.tex"], _log, cwd=tmpdir)

            with (tmppath / "figure.pdf").open("rb") as orig, \
                 cbook.open_file_cm(fname_or_fh, "wb") as dest:
                shutil.copyfileobj(orig, dest)  # copy file contents to target
