    def _get_font_afm(self, prop):
        key = hash(prop)
        font = self.afm_font_cache.get(key)
        if font is None:
            filename = findfont(
                prop, fontext='afm', directory=self.file._core14fontdir)
            if filename is None:
                filename = findfont(
                    "Helvetica", fontext='afm',
                    directory=self.file._core14fontdir)
            font = self.afm_font_cache.get(filename)
            if font is None:
                with open(filename, 'rb') as fh:
                    font = AFM(fh)
                    self.afm_font_cache[filename] = font
            self.afm_font_cache[key] = font
        return font
