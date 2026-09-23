    def _get_font(self, font: str | int) -> FT2Font:
        if font in self.fontmap:
            basename = self.fontmap[font]
        else:
            # NOTE: An int is only passed by subclasses which have placed int keys into
            # `self.fontmap`, so we must cast this to confirm it to typing.
            basename = T.cast(str, font)
        cached_font = self._fonts.get(basename)
        if cached_font is None and os.path.exists(basename):
            cached_font = get_font(basename)
            self._fonts[basename] = cached_font
            self._fonts[cached_font.postscript_name] = cached_font
            self._fonts[cached_font.postscript_name.lower()] = cached_font
        return T.cast(FT2Font, cached_font)  # FIXME: Not sure this is guaranteed.
