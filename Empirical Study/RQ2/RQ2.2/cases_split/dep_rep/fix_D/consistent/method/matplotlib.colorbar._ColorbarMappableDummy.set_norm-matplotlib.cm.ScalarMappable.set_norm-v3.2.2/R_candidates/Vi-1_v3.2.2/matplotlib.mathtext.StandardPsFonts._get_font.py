    def _get_font(self, font):
        if font in self.fontmap:
            basename = self.fontmap[font]
        else:
            basename = font

        cached_font = self.fonts.get(basename)
        if cached_font is None:
            fname = os.path.join(self.basepath, basename + ".afm")
            with open(fname, 'rb') as fd:
                cached_font = AFM(fd)
            cached_font.fname = fname
            self.fonts[basename] = cached_font
            self.fonts[cached_font.get_fontname()] = cached_font
        return cached_font
