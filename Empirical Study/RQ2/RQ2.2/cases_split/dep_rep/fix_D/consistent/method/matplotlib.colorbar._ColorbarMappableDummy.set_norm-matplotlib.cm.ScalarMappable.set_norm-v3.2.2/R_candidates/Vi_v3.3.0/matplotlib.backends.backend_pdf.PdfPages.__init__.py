    def __init__(self, filename, keep_empty=True, metadata=None):
        """
        Create a new PdfPages object.

        Parameters
        ----------
        filename : str or path-like or file-like
            Plots using `PdfPages.savefig` will be written to a file at this
            location. The file is opened at once and any older file with the
            same name is overwritten.
        keep_empty : bool, optional
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
        """
        self._file = PdfFile(filename, metadata=metadata)
        self.keep_empty = keep_empty
