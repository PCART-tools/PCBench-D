class PdfPages:
    """
    A multi-page PDF file using the pgf backend

    Examples
    --------

    >>> import matplotlib.pyplot as plt
    >>> # Initialize:
    >>> with PdfPages('foo.pdf') as pdf:
    ...     # As many times as you like, create a figure fig and save it:
    ...     fig = plt.figure()
    ...     pdf.savefig(fig)
    ...     # When no figure is specified the current figure is saved
    ...     pdf.savefig()
    """
    __slots__ = (
        '_outputfile',
        'keep_empty',
        '_tmpdir',
        '_basename',
        '_fname_tex',
        '_fname_pdf',
        '_n_figures',
        '_file',
        'metadata',
    )

    def __init__(self, filename, *, keep_empty=True, metadata=None):
        """
        Create a new PdfPages object.

        Parameters
        ----------

        filename : str
            Plots using :meth:`PdfPages.savefig` will be written to a file at
            this location. Any older file with the same name is overwritten.
        keep_empty : bool, optional
            If set to False, then empty pdf files will be deleted automatically
            when closed.
        metadata : dictionary, optional
            Information dictionary object (see PDF reference section 10.2.1
            'Document Information Dictionary'), e.g.:
            `{'Creator': 'My software', 'Author': 'Me',
            'Title': 'Awesome fig'}`

            The standard keys are `'Title'`, `'Author'`, `'Subject'`,
            `'Keywords'`, `'Producer'`, `'Creator'` and `'Trapped'`.
            Values have been predefined for `'Creator'` and `'Producer'`.
            They can be removed by setting them to the empty string.
        """
        self._outputfile = filename
        self._n_figures = 0
        self.keep_empty = keep_empty
        self.metadata = metadata or {}

        # create temporary directory for compiling the figure
        self._tmpdir = tempfile.mkdtemp(prefix="mpl_pgf_pdfpages_")
        self._basename = 'pdf_pages'
        self._fname_tex = os.path.join(self._tmpdir, self._basename + ".tex")
        self._fname_pdf = os.path.join(self._tmpdir, self._basename + ".pdf")
        self._file = open(self._fname_tex, 'wb')

    def _write_header(self, width_inches, height_inches):
        supported_keys = {
            'title', 'author', 'subject', 'keywords', 'creator',
            'producer', 'trapped'
        }
        infoDict = {
            'creator': 'matplotlib %s, https://matplotlib.org' % __version__,
            'producer': 'matplotlib pgf backend %s' % __version__,
        }
        metadata = {k.lower(): v for k, v in self.metadata.items()}
        infoDict.update(metadata)
        hyperref_options = ''
        for k, v in infoDict.items():
            if k not in supported_keys:
                raise ValueError(
                    'Not a supported pdf metadata field: "{}"'.format(k)
                )
            hyperref_options += 'pdf' + k + '={' + str(v) + '},'

        latex_preamble = get_preamble()
        latex_fontspec = get_fontspec()
        latex_header = r"""\PassOptionsToPackage{{
  {metadata}
}}{{hyperref}}
\RequirePackage{{hyperref}}
\documentclass[12pt]{{minimal}}
\usepackage[
    paperwidth={width}in,
    paperheight={height}in,
    margin=0in
]{{geometry}}
{preamble}
{fontspec}
\usepackage{{pgf}}
\setlength{{\parindent}}{{0pt}}

\begin{{document}}%%
""".format(
            width=width_inches,
            height=height_inches,
            preamble=latex_preamble,
            fontspec=latex_fontspec,
            metadata=hyperref_options,
        )
        self._file.write(latex_header.encode('utf-8'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Finalize this object, running LaTeX in a temporary directory
        and moving the final pdf file to `filename`.
        """
        self._file.write(rb'\end{document}\n')
        self._file.close()

        if self._n_figures > 0:
            try:
                self._run_latex()
            finally:
                try:
                    shutil.rmtree(self._tmpdir)
                except:
                    TmpDirCleaner.add(self._tmpdir)
        elif self.keep_empty:
            open(self._outputfile, 'wb').close()

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

    def savefig(self, figure=None, **kwargs):
        """
        Saves a :class:`~matplotlib.figure.Figure` to this file as a new page.

        Any other keyword arguments are passed to
        :meth:`~matplotlib.figure.Figure.savefig`.

        Parameters
        ----------

        figure : :class:`~matplotlib.figure.Figure` or int, optional
            Specifies what figure is saved to file. If not specified, the
            active figure is saved. If a :class:`~matplotlib.figure.Figure`
            instance is provided, this figure is saved. If an int is specified,
            the figure instance to save is looked up by number.
        """
        if not isinstance(figure, Figure):
            if figure is None:
                manager = Gcf.get_active()
            else:
                manager = Gcf.get_fig_manager(figure)
            if manager is None:
                raise ValueError("No figure {}".format(figure))
            figure = manager.canvas.figure

        try:
            orig_canvas = figure.canvas
            figure.canvas = FigureCanvasPgf(figure)

            width, height = figure.get_size_inches()
            if self._n_figures == 0:
                self._write_header(width, height)
            else:
                # \pdfpagewidth and \pdfpageheight exist on pdftex, xetex, and
                # luatex<0.85; they were renamed to \pagewidth and \pageheight
                # on luatex>=0.85.
                self._file.write(
                    br'\newpage'
                    br'\ifdefined\pdfpagewidth\pdfpagewidth'
                    br'\else\pagewidth\fi=%ain'
                    br'\ifdefined\pdfpageheight\pdfpageheight'
                    br'\else\pageheight\fi=%ain'
                    b'%%\n' % (width, height)
                )

            figure.savefig(self._file, format="pgf", **kwargs)
            self._n_figures += 1
        finally:
            figure.canvas = orig_canvas

    def get_pagecount(self):
        """
        Returns the current number of pages in the multipage pdf file.
        """
        return self._n_figures
