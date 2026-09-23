    def __init__(self, width, height, svgwriter, basename=None, image_dpi=72,
                 *, metadata=None):
        self.width = width
        self.height = height
        self.writer = XMLWriter(svgwriter)
        self.image_dpi = image_dpi  # actual dpi at which we rasterize stuff

        if basename is None:
            basename = getattr(svgwriter, "name", "")
            if not isinstance(basename, str):
                basename = ""
        self.basename = basename

        self._groupd = {}
        self._image_counter = itertools.count()
        self._clipd = {}
        self._markers = {}
        self._path_collection_id = 0
        self._hatchd = {}
        self._has_gouraud = False
        self._n_gradients = 0

        super().__init__()
        self._glyph_map = dict()
        str_height = _short_float_fmt(height)
        str_width = _short_float_fmt(width)
        svgwriter.write(svgProlog)
        self._start_id = self.writer.start(
            'svg',
            width=f'{str_width}pt',
            height=f'{str_height}pt',
            viewBox=f'0 0 {str_width} {str_height}',
            xmlns="http://www.w3.org/2000/svg",
            version="1.1",
            attrib={'xmlns:xlink': "http://www.w3.org/1999/xlink"})
        self._write_metadata(metadata)
        self._write_default_style()
