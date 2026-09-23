    def __init__(self, default_font_prop):
        Fonts.__init__(self, default_font_prop, MathtextBackendPs())
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
        self.pswriter = StringIO()
