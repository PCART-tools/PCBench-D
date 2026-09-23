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
