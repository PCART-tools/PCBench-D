class FigureCanvasPgf(FigureCanvasBase):
    filetypes = {"pgf": "LaTeX PGF picture",
                 "pdf": "LaTeX compiled PGF picture",
                 "png": "Portable Network Graphics", }

    def get_default_filetype(self):
        return 'pdf'

    @_check_savefig_extra_args
    def _print_pgf_to_fh(self, fh, *, bbox_inches_restore=None):

        header_text = """%% Creator: Matplotlib, PGF backend
%%
%% To include the figure in your LaTeX document, write
%%   \\input{<filename>.pgf}
%%
%% Make sure the required packages are loaded in your preamble
%%   \\usepackage{pgf}
%%
%% Figures using additional raster images can only be included by \\input if
%% they are in the same directory as the main LaTeX file. For loading figures
%% from other directories you can use the `import` package
%%   \\usepackage{import}
%%
%% and then include the figures with
%%   \\import{<path to file>}{<filename>.pgf}
%%
"""

        # append the preamble used by the backend as a comment for debugging
        header_info_preamble = ["%% Matplotlib used the following preamble"]
        for line in get_preamble().splitlines():
            header_info_preamble.append("%%   " + line)
        for line in get_fontspec().splitlines():
            header_info_preamble.append("%%   " + line)
        header_info_preamble.append("%%")
        header_info_preamble = "\n".join(header_info_preamble)

        # get figure size in inch
        w, h = self.figure.get_figwidth(), self.figure.get_figheight()
        dpi = self.figure.get_dpi()

        # create pgfpicture environment and write the pgf code
        fh.write(header_text)
        fh.write(header_info_preamble)
        fh.write("\n")
        writeln(fh, r"\begingroup")
        writeln(fh, r"\makeatletter")
        writeln(fh, r"\begin{pgfpicture}")
        writeln(fh,
                r"\pgfpathrectangle{\pgfpointorigin}{\pgfqpoint{%fin}{%fin}}"
                % (w, h))
        writeln(fh, r"\pgfusepath{use as bounding box, clip}")
        renderer = MixedModeRenderer(self.figure, w, h, dpi,
                                     RendererPgf(self.figure, fh),
                                     bbox_inches_restore=bbox_inches_restore)
        self.figure.draw(renderer)

        # end the pgfpicture environment
        writeln(fh, r"\end{pgfpicture}")
        writeln(fh, r"\makeatother")
        writeln(fh, r"\endgroup")

    def print_pgf(self, fname_or_fh, *args, **kwargs):
        """
        Output pgf macros for drawing the figure so it can be included and
        rendered in latex documents.
        """
        with cbook.open_file_cm(fname_or_fh, "w", encoding="utf-8") as file:
            if not cbook.file_requires_unicode(file):
                file = codecs.getwriter("utf-8")(file)
            self._print_pgf_to_fh(file, *args, **kwargs)

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

    def print_png(self, fname_or_fh, *args, **kwargs):
        """Use LaTeX to compile a pgf figure to pdf and convert it to png."""
        converter = make_pdf_to_png_converter()
        with TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)
            pdf_path = tmppath / "figure.pdf"
            png_path = tmppath / "figure.png"
            self.print_pdf(pdf_path, *args, **kwargs)
            converter(pdf_path, png_path, dpi=self.figure.dpi)
            with png_path.open("rb") as orig, \
                 cbook.open_file_cm(fname_or_fh, "wb") as dest:
                shutil.copyfileobj(orig, dest)  # copy file contents to target

    def get_renderer(self):
        return RendererPgf(self.figure, None)

    def draw(self):
        _no_output_draw(self.figure)
        return super().draw()
