    def __init__(self, filename, metadata=None):
        self.nextObject = 1     # next free object id
        self.xrefTable = [[0, 65535, 'the zero object']]
        self.passed_in_file_object = False
        self.original_file_like = None
        self.tell_base = 0
        if isinstance(filename, six.string_types):
            fh = open(filename, 'wb')
        elif is_writable_file_like(filename):
            try:
                self.tell_base = filename.tell()
            except IOError:
                fh = BytesIO()
                self.original_file_like = filename
            else:
                fh = filename
                self.passed_in_file_object = True
        else:
            raise ValueError("filename must be a path or a file-like object")

        self._core14fontdir = os.path.join(
            rcParams['datapath'], 'fonts', 'pdfcorefonts')
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
        self.alphaStateObject = self.reserveObject('extended graphics states')
        self.hatchObject = self.reserveObject('tiling patterns')
        self.gouraudObject = self.reserveObject('Gouraud triangles')
        self.XObjectObject = self.reserveObject('external objects')
        self.resourceObject = self.reserveObject('resources')

        root = {'Type': Name('Catalog'),
                'Pages': self.pagesObject}
        self.writeObject(self.rootObject, root)

        # get source date from SOURCE_DATE_EPOCH, if set
        # See https://reproducible-builds.org/specs/source-date-epoch/
        source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
        if source_date_epoch:
            source_date = datetime.utcfromtimestamp(int(source_date_epoch))
            source_date = source_date.replace(tzinfo=UTC)
        else:
            source_date = datetime.today()

        self.infoDict = {
            'Creator': 'matplotlib %s, http://matplotlib.org' % __version__,
            'Producer': 'matplotlib pdf backend %s' % __version__,
            'CreationDate': source_date
        }
        if metadata is not None:
            self.infoDict.update(metadata)
        self.infoDict = {k: v for (k, v) in self.infoDict.items()
                         if v is not None}

        self.fontNames = {}     # maps filenames to internal font names
        self.nextFont = 1       # next free internal font name
        self.dviFontInfo = {}   # maps dvi font names to embedding information
        self._texFontMap = None  # maps TeX font names to PostScript fonts
        # differently encoded Type-1 fonts may share the same descriptor
        self.type1Descriptors = {}
        self.used_characters = {}

        self.alphaStates = {}   # maps alpha values to graphics state objects
        self.nextAlphaState = 1
        # reproducible writeHatches needs an ordered dict:
        self.hatchPatterns = collections.OrderedDict()
        self.nextHatch = 1
        self.gouraudTriangles = []

        self._images = collections.OrderedDict()   # reproducible writeImages
        self.nextImage = 1

        self.markers = collections.OrderedDict()   # reproducible writeMarkers
        self.multi_byte_charprocs = {}

        self.paths = []

        self.pageAnnotations = []  # A list of annotations for the
                                   # current page

        # The PDF spec recommends to include every procset
        procsets = [Name(x)
                    for x in "PDF Text ImageB ImageC ImageI".split()]

        # Write resource dictionary.
        # Possibly TODO: more general ExtGState (graphics state dictionaries)
        #                ColorSpace Pattern Shading Properties
        resources = {'Font': self.fontObject,
                     'XObject': self.XObjectObject,
                     'ExtGState': self.alphaStateObject,
                     'Pattern': self.hatchObject,
                     'Shading': self.gouraudObject,
                     'ProcSet': procsets}
        self.writeObject(self.resourceObject, resources)
