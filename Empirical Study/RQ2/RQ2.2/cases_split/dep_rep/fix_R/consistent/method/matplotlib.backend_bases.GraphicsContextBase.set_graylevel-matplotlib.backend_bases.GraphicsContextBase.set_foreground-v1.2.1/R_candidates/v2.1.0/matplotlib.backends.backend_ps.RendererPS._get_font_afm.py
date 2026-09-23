    def _get_font_afm(self, prop):
        key = hash(prop)
        font = self.afmfontd.get(key)
        if font is None:
            fname = findfont(prop, fontext='afm', directory=self._afm_font_dir)
            if fname is None:
                fname = findfont(
                    "Helvetica", fontext='afm', directory=self._afm_font_dir)
            font = self.afmfontd.get(fname)
            if font is None:
                with io.open(fname, 'rb') as fh:
                    font = AFM(fh)
                self.afmfontd[fname] = font
            self.afmfontd[key] = font
        return font
