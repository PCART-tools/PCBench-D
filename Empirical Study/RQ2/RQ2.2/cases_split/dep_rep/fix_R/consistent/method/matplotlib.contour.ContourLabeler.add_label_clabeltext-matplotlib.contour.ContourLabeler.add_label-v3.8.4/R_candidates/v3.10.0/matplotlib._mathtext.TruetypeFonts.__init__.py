    def __init__(self, default_font_prop: FontProperties, load_glyph_flags: LoadFlags):
        super().__init__(default_font_prop, load_glyph_flags)
        # Per-instance cache.
        self._get_info = functools.cache(self._get_info)  # type: ignore[method-assign]
        self._fonts = {}
        self.fontmap: dict[str | int, str] = {}

        filename = findfont(self.default_font_prop)
        default_font = get_font(filename)
        self._fonts['default'] = default_font
        self._fonts['regular'] = default_font
