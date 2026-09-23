    def writeFonts(self):
        fonts = {}
        for dviname, info in sorted(self.dviFontInfo.items()):
            Fx = info.pdfname
            matplotlib.verbose.report('Embedding Type-1 font %s from dvi'
                                      % dviname, 'debug')
            fonts[Fx] = self._embedTeXFont(info)
        for filename in sorted(self.fontNames):
            Fx = self.fontNames[filename]
            matplotlib.verbose.report('Embedding font %s' % filename, 'debug')
            if filename.endswith('.afm'):
                # from pdf.use14corefonts
                matplotlib.verbose.report('Writing AFM font', 'debug')
                fonts[Fx] = self._write_afm_font(filename)
            else:
                # a normal TrueType font
                matplotlib.verbose.report('Writing TrueType font', 'debug')
                realpath, stat_key = get_realpath_and_stat(filename)
                chars = self.used_characters.get(stat_key)
                if chars is not None and len(chars[1]):
                    fonts[Fx] = self.embedTTF(realpath, chars[1])
        self.writeObject(self.fontObject, fonts)
