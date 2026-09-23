    def print_pdf(self, fname_or_fh, *, metadata=None, **kwargs):
        """Use LaTeX to compile a pgf generated figure to pdf."""
        w, h = self.figure.get_size_inches()

        info_dict = _create_pdf_info_dict('pgf', metadata or {})
        pdfinfo = ','.join(
            _metadata_to_str(k, v) for k, v in info_dict.items())

        # print figure to pgf and compile it with latex
        with TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)
            self.print_pgf(tmppath / "figure.pgf", **kwargs)
            (tmppath / "figure.tex").write_text(
                "\n".join([
                    r"\PassOptionsToPackage{pdfinfo={%s}}{hyperref}" % pdfinfo,
                    r"\RequirePackage{hyperref}",
                    r"\documentclass[12pt]{minimal}",
                    r"\usepackage[papersize={%fin,%fin}, margin=0in]{geometry}"
                    % (w, h),
                    get_preamble(),
                    get_fontspec(),
                    r"\usepackage{pgf}",
                    r"\begin{document}",
                    r"\centering",
                    r"\input{figure.pgf}",
                    r"\end{document}",
                ]), encoding="utf-8")
            texcommand = mpl.rcParams["pgf.texsystem"]
            cbook._check_and_log_subprocess(
                [texcommand, "-interaction=nonstopmode", "-halt-on-error",
                 "figure.tex"], _log, cwd=tmpdir)
            with (tmppath / "figure.pdf").open("rb") as orig, \
                 cbook.open_file_cm(fname_or_fh, "wb") as dest:
                shutil.copyfileobj(orig, dest)  # copy file contents to target
