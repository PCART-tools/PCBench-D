    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Per-instance cache.
        self._get_info = functools.lru_cache(None)(self._get_info)
        self._fonts = {}

        filename = findfont(self.default_font_prop)
        default_font = get_font(filename)
        self._fonts['default'] = default_font
        self._fonts['regular'] = default_font
