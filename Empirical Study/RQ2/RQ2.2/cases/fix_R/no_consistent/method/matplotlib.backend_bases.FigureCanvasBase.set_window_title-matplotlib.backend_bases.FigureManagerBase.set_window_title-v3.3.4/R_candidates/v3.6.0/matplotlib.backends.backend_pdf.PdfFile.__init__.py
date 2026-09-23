    def __init__(self, filename, metadata=None):
        """
        Parameters
        ----------
        filename : str or path-like or file-like
            Output target; if a string, a file will be opened for writing.

        metadata : dict from strings to strings and dates
            Information dictionary object (see PDF reference section 10.2.1
            'Document Information Dictionary'), e.g.:
            ``{'Creator': 'My software', 'Author': 'Me', 'Title': 'Awesome'}``.

            The standard keys are 'Title', 'Author', 'Subject', 'Keywords',
            'Creator', 'Producer', 'CreationDate', 'ModDate', and
            'Trapped'. Values have been predefined for 'Creator', 'Producer'
            and 'CreationDate'. They can be removed by setting them to `None`.
        """
        super().__init__()

        self._object_seq = itertools.count(1)  # consumed by reserveObject
        self.xrefTable = [[0, 65535, 'the zero object']]
        self.passed_in_file_object = False
        self.original_file_like = None
        self.tell_base = 0
        fh, opened = cbook.to_filehandle(filename, "wb", return_opened=True)
        if not opened:
            try:
                self.tell_base = filename.tell()
            except IOError:
                fh = BytesIO()
                self.original_file_like = filename
            else:
                fh = filename
                self.passed_in_file_object = True

        self.fh = fh
        self.currentstream = None  # stream object to write to, if any
        fh.write(b"%PDF-1.4\n")    # 1.4 is the first version to have alpha
        # Output some eight-bit chars as a comment so various utilities
        # recognize the file as binary by looking at the first few
        # lines (see note in section 3.4.1 of the PDF reference).
        fh.write(b"%\254\334 \253\272\n")

        self.rootObject = self.reserveObject('root')
        self.pagesObject = self.reserveObject('pages')
        self.pageList = []
        self.fontObject = self.reserveObject('fonts')
        self._extGStateObject = self.reserveObject('extended graphics states')
        self.hatchObject = self.reserveObject('tiling patterns')
        self.gouraudObject = self.reserveObject('Gouraud triangles')
        self.XObjectObject = self.reserveObject('external objects')
        self.resourceObject = self.reserveObject('resources')

        root = {'Type': Name('Catalog'),
                'Pages': self.pagesObject}
        self.writeObject(self.rootObject, root)

        self.infoDict = _create_pdf_info_dict('pdf', metadata or {})

        self.fontNames = {}     # maps filenames to internal font names
        self._internal_font_seq = (Name(f'F{i}') for i in itertools.count(1))
        self.dviFontInfo = {}   # maps dvi font names to embedding information
        # differently encoded Type-1 fonts may share the same descriptor
        self.type1Descriptors = {}
        self._character_tracker = _backend_pdf_ps.CharacterTracker()

        self.alphaStates = {}   # maps alpha values to graphics state objects
        self._alpha_state_seq = (Name(f'A{i}') for i in itertools.count(1))
        self._soft_mask_states = {}
        self._soft_mask_seq = (Name(f'SM{i}') for i in itertools.count(1))
        self._soft_mask_groups = []
        self.hatchPatterns = {}
        self._hatch_pattern_seq = (Name(f'H{i}') for i in itertools.count(1))
        self.gouraudTriangles = []

        self._images = {}
        self._image_seq = (Name(f'I{i}') for i in itertools.count(1))

        self.markers = {}
        self.multi_byte_charprocs = {}

        self.paths = []

        # A list of annotations for each page. Each entry is a tuple of the
        # overall Annots object reference that's inserted into the page object,
        # followed by a list of the actual annotations.
        self._annotations = []
        # For annotations added before a page is created; mostly for the
        # purpose of newTextnote.
        self.pageAnnotations = []

        # The PDF spec recommends to include every procset
        procsets = [Name(x) for x in "PDF Text ImageB ImageC ImageI".split()]

        # Write resource dictionary.
        # Possibly TODO: more general ExtGState (graphics state dictionaries)
        #                ColorSpace Pattern Shading Properties
        resources = {'Font': self.fontObject,
                     'XObject': self.XObjectObject,
                     'ExtGState': self._extGStateObject,
                     'Pattern': self.hatchObject,
                     'Shading': self.gouraudObject,
                     'ProcSet': procsets}
        self.writeObject(self.resourceObject, resources)
