    def __init__(self, default_font_prop, mathtext_backend):
        Fonts.__init__(self, default_font_prop, mathtext_backend)
        self.glyphd = {}
        self._fonts = {}

        filename = findfont(default_font_prop)
        default_font = get_font(filename)
        self._fonts['default'] = default_font
        self._fonts['regular'] = default_font
