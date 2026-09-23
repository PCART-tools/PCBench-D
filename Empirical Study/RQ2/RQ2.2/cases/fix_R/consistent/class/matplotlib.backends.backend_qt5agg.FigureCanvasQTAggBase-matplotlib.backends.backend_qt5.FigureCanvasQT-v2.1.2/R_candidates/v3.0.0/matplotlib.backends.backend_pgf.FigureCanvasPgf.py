class FigureCanvasPgf(FigureCanvasBase):
    filetypes = {"pgf": "LaTeX PGF picture",
                 "pdf": "LaTeX compiled PGF picture",
                 "png": "Portable Network Graphics", }

    def get_default_filetype(self):
        return 'pdf'

    def _print_pgf_to_fh(self, fh, *args,
                         dryrun=False, bbox_inches_restore=None, **kwargs):
        if dryrun:
            renderer = RendererPgf(self.figure, None, dummy=True)
            self.figure.draw(renderer)
            return

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
        Output pgf commands for drawing the figure so it can be included and
        rendered in latex documents.
        """
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return

        # figure out where the pgf is to be written to
        if isinstance(fname_or_fh, str):
            with open(fname_or_fh, "w", encoding="utf-8") as fh:
                self._print_pgf_to_fh(fh, *args, **kwargs)
        elif is_writable_file_like(fname_or_fh):
            fh = codecs.getwriter("utf-8")(fname_or_fh)
            self._print_pgf_to_fh(fh, *args, **kwargs)
        else:
            raise ValueError("filename must be a path")

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
            pathlib.Path(fname_tex).write_text(latexcode, encoding="utf-8")

            texcommand = rcParams["pgf.texsystem"]
            cmdargs = [texcommand, "-interaction=nonstopmode",
                       "-halt-on-error", "figure.tex"]
            try:
                subprocess.check_output(
                    cmdargs, stderr=subprocess.STDOUT, cwd=tmpdir)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    "%s was not able to process your file.\n\nFull log:\n%s"
                    % (texcommand, e.output))

            # copy file contents to target
            with open(fname_pdf, "rb") as fh_src:
                shutil.copyfileobj(fh_src, fh)
        finally:
            try:
                shutil.rmtree(tmpdir)
            except:
                TmpDirCleaner.add(tmpdir)

    def print_pdf(self, fname_or_fh, *args, **kwargs):
        """
        Use LaTeX to compile a Pgf generated figure to PDF.
        """
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return

        # figure out where the pdf is to be written to
        if isinstance(fname_or_fh, str):
            with open(fname_or_fh, "wb") as fh:
                self._print_pdf_to_fh(fh, *args, **kwargs)
        elif is_writable_file_like(fname_or_fh):
            self._print_pdf_to_fh(fname_or_fh, *args, **kwargs)
        else:
            raise ValueError("filename must be a path or a file-like object")

    def _print_png_to_fh(self, fh, *args, **kwargs):
        converter = make_pdf_to_png_converter()

        try:
            # create temporary directory for pdf creation and png conversion
            tmpdir = tempfile.mkdtemp(prefix="mpl_pgf_")
            fname_pdf = os.path.join(tmpdir, "figure.pdf")
            fname_png = os.path.join(tmpdir, "figure.png")
            # create pdf and try to convert it to png
            self.print_pdf(fname_pdf, *args, **kwargs)
            converter(fname_pdf, fname_png, dpi=self.figure.dpi)
            # copy file contents to target
            with open(fname_png, "rb") as fh_src:
                shutil.copyfileobj(fh_src, fh)
        finally:
            try:
                shutil.rmtree(tmpdir)
            except:
                TmpDirCleaner.add(tmpdir)

    def print_png(self, fname_or_fh, *args, **kwargs):
        """
        Use LaTeX to compile a pgf figure to pdf and convert it to png.
        """
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return

        if isinstance(fname_or_fh, str):
            with open(fname_or_fh, "wb") as fh:
                self._print_png_to_fh(fh, *args, **kwargs)
        elif is_writable_file_like(fname_or_fh):
            self._print_png_to_fh(fname_or_fh, *args, **kwargs)
        else:
            raise ValueError("filename must be a path or a file-like object")

    def get_renderer(self):
        return RendererPgf(self.figure, None, dummy=True)
