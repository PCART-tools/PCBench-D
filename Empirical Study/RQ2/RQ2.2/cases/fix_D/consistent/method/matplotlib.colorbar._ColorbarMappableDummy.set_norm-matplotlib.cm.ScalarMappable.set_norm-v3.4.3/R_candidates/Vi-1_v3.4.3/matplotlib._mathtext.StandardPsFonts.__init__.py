    def __init__(self, default_font_prop, mathtext_backend=None):
        if mathtext_backend is None:
            # Circular import, can be dropped after public access to
            # StandardPsFonts is removed and mathtext_backend made a required
            # parameter.
            from . import mathtext
            mathtext_backend = mathtext.MathtextBackendPath()
        super().__init__(default_font_prop, mathtext_backend)
        self.glyphd = {}
        self.fonts = {}

        filename = findfont(default_font_prop, fontext='afm',
                            directory=self.basepath)
        if filename is None:
            filename = findfont('Helvetica', fontext='afm',
                                directory=self.basepath)
        with open(filename, 'rb') as fd:
            default_font = AFM(fd)
        default_font.fname = filename

        self.fonts['default'] = default_font
        self.fonts['regular'] = default_font
