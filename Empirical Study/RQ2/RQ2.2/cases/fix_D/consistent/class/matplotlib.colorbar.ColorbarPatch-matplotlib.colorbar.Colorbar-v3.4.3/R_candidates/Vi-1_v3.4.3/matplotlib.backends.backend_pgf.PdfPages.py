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
        '_output_name',
        'keep_empty',
        '_n_figures',
        '_file',
        '_info_dict',
        '_metadata',
    )
    metadata = _api.deprecated('3.3')(property(lambda self: self._metadata))

    def __init__(self, filename, *, keep_empty=True, metadata=None):
        """
        Create a new PdfPages object.

        Parameters
        ----------
        filename : str or path-like
            Plots using `PdfPages.savefig` will be written to a file at this
            location. Any older file with the same name is overwritten.

        keep_empty : bool, default: True
            If set to False, then empty pdf files will be deleted automatically
            when closed.

        metadata : dict, optional
            Information dictionary object (see PDF reference section 10.2.1
            'Document Information Dictionary'), e.g.:
            ``{'Creator': 'My software', 'Author': 'Me', 'Title': 'Awesome'}``.

            The standard keys are 'Title', 'Author', 'Subject', 'Keywords',
            'Creator', 'Producer', 'CreationDate', 'ModDate', and
            'Trapped'. Values have been predefined for 'Creator', 'Producer'
            and 'CreationDate'. They can be removed by setting them to `None`.

            Note that some versions of LaTeX engines may ignore the 'Producer'
            key and set it to themselves.
        """
        self._output_name = filename
        self._n_figures = 0
        self.keep_empty = keep_empty
        self._metadata = (metadata or {}).copy()
        if metadata:
            for key in metadata:
                canonical = {
                    'creationdate': 'CreationDate',
                    'moddate': 'ModDate',
                }.get(key.lower(), key.lower().title())
                if canonical != key:
                    _api.warn_deprecated(
                        '3.3', message='Support for setting PDF metadata keys '
                        'case-insensitively is deprecated since %(since)s and '
                        'will be removed %(removal)s; '
                        f'set {canonical} instead of {key}.')
                    self._metadata[canonical] = self._metadata.pop(key)
        self._info_dict = _create_pdf_info_dict('pgf', self._metadata)
        self._file = BytesIO()

    def _write_header(self, width_inches, height_inches):
        hyperref_options = ','.join(
            _metadata_to_str(k, v) for k, v in self._info_dict.items())

        latex_preamble = get_preamble()
        latex_fontspec = get_fontspec()
        latex_header = r"""\PassOptionsToPackage{{
  pdfinfo={{
    {metadata}
  }}
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
        and moving the final pdf file to *filename*.
        """
        self._file.write(rb'\end{document}\n')
        if self._n_figures > 0:
            self._run_latex()
        elif self.keep_empty:
            open(self._output_name, 'wb').close()
        self._file.close()

    def _run_latex(self):
        texcommand = mpl.rcParams["pgf.texsystem"]
        with TemporaryDirectory() as tmpdir:
            tex_source = pathlib.Path(tmpdir, "pdf_pages.tex")
            tex_source.write_bytes(self._file.getvalue())
            cbook._check_and_log_subprocess(
                [texcommand, "-interaction=nonstopmode", "-halt-on-error",
                 tex_source],
                _log, cwd=tmpdir)
            shutil.move(tex_source.with_suffix(".pdf"), self._output_name)

    def savefig(self, figure=None, **kwargs):
        """
        Save a `.Figure` to this file as a new page.

        Any other keyword arguments are passed to `~.Figure.savefig`.

        Parameters
        ----------
        figure : `.Figure` or int, optional
            Specifies what figure is saved to file. If not specified, the
            active figure is saved. If a `.Figure` instance is provided, this
            figure is saved. If an int is specified, the figure instance to
            save is looked up by number.
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
        """Return the current number of pages in the multipage pdf file."""
        return self._n_figures
