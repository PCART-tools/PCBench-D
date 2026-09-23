    def writeFonts(self):
        fonts = {}
        for dviname, info in sorted(self.dviFontInfo.items()):
            Fx = info.pdfname
            _log.debug('Embedding Type-1 font %s from dvi.', dviname)
            fonts[Fx] = self._embedTeXFont(info)
        for filename in sorted(self.fontNames):
            Fx = self.fontNames[filename]
            _log.debug('Embedding font %s.', filename)
            if filename.endswith('.afm'):
                # from pdf.use14corefonts
                _log.debug('Writing AFM font.')
                fonts[Fx] = self._write_afm_font(filename)
            else:
                # a normal TrueType font
                _log.debug('Writing TrueType font.')
                realpath, stat_key = cbook.get_realpath_and_stat(filename)
                chars = self.used_characters.get(stat_key)
                if chars is not None and len(chars[1]):
                    fonts[Fx] = self.embedTTF(realpath, chars[1])
        self.writeObject(self.fontObject, fonts)
