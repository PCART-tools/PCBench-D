    def __init__(self, filename, *, keep_empty=True, metadata=None):
        """
        Create a new PdfPages object.

        Parameters
        ----------
        filename : str or path-like
            Plots using `PdfPages.savefig` will be written to a file at this
            location. Any older file with the same name is overwritten.
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
