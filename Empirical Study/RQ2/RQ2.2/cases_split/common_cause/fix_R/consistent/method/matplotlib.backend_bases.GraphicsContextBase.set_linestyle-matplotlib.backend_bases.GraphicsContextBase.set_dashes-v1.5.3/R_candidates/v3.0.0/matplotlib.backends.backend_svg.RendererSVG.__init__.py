    def __init__(self, width, height, svgwriter, basename=None, image_dpi=72):
        self.width = width
        self.height = height
        self.writer = XMLWriter(svgwriter)
        self.image_dpi = image_dpi  # the actual dpi we want to rasterize stuff with

        self._groupd = {}
        if not rcParams['svg.image_inline']:
            assert basename is not None
            self.basename = basename
            self._imaged = {}
        self._clipd = OrderedDict()
        self._char_defs = {}
        self._markers = {}
        self._path_collection_id = 0
        self._imaged = {}
        self._hatchd = OrderedDict()
        self._has_gouraud = False
        self._n_gradients = 0
        self._fonts = OrderedDict()
        self.mathtext_parser = MathTextParser('SVG')

        RendererBase.__init__(self)
        self._glyph_map = dict()
        str_height = short_float_fmt(height)
        str_width = short_float_fmt(width)
        svgwriter.write(svgProlog)
        self._start_id = self.writer.start(
            'svg',
            width='%spt' % str_width,
            height='%spt' % str_height,
            viewBox='0 0 %s %s' % (str_width, str_height),
            xmlns="http://www.w3.org/2000/svg",
            version="1.1",
            attrib={'xmlns:xlink': "http://www.w3.org/1999/xlink"})
        self._write_default_style()
