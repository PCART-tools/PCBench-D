class PdfPages(object):
    """
    A multi-page PDF file.

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

    Notes
    -----

    In reality :class:`PdfPages` is a thin wrapper around :class:`PdfFile`, in
    order to avoid confusion when using :func:`~matplotlib.pyplot.savefig` and
    forgetting the format argument.
    """
    __slots__ = ('_file', 'keep_empty')

    def __init__(self, filename, keep_empty=True, metadata=None):
        """
        Create a new PdfPages object.

        Parameters
        ----------

        filename : str
            Plots using :meth:`PdfPages.savefig` will be written to a file at
            this location. The file is opened at once and any older file with
            the same name is overwritten.
        keep_empty : bool, optional
            If set to False, then empty pdf files will be deleted automatically
            when closed.
        metadata : dictionary, optional
            Information dictionary object (see PDF reference section 10.2.1
            'Document Information Dictionary'), e.g.:
            `{'Creator': 'My software', 'Author': 'Me',
            'Title': 'Awesome fig'}`

            The standard keys are `'Title'`, `'Author'`, `'Subject'`,
            `'Keywords'`, `'Creator'`, `'Producer'`, `'CreationDate'`,
            `'ModDate'`, and `'Trapped'`. Values have been predefined
            for `'Creator'`, `'Producer'` and `'CreationDate'`. They
            can be removed by setting them to `None`.

        """
        self._file = PdfFile(filename, metadata=metadata)
        self.keep_empty = keep_empty

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Finalize this object, making the underlying file a complete
        PDF file.
        """
        self._file.finalize()
        self._file.close()
        if (self.get_pagecount() == 0 and not self.keep_empty and
                not self._file.passed_in_file_object):
            os.remove(self._file.fh.name)
        self._file = None

    def infodict(self):
        """
        Return a modifiable information dictionary object
        (see PDF reference section 10.2.1 'Document Information
        Dictionary').
        """
        return self._file.infoDict

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
        # Force use of pdf backend, as PdfPages is tightly coupled with it.
        try:
            orig_canvas = figure.canvas
            figure.canvas = FigureCanvasPdf(figure)
            figure.savefig(self, format="pdf", **kwargs)
        finally:
            figure.canvas = orig_canvas

    def get_pagecount(self):
        """
        Returns the current number of pages in the multipage pdf file.
        """
        return len(self._file.pageList)

    def attach_note(self, text, positionRect=[-100, -100, 0, 0]):
        """
        Add a new text note to the page to be saved next. The optional
        positionRect specifies the position of the new note on the
        page. It is outside the page per default to make sure it is
        invisible on printouts.
        """
        self._file.newTextnote(text, positionRect)
