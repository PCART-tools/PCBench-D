    def dviFontName(self, dvifont):
        """
        Given a dvi font object, return a name suitable for Op.selectfont.
        This registers the font information in self.dviFontInfo if not yet
        registered.
        """

        dvi_info = self.dviFontInfo.get(dvifont.texname)
        if dvi_info is not None:
            return dvi_info.pdfname

        psfont = self.texFontMap[dvifont.texname]
        if psfont.filename is None:
            raise ValueError(
                ("No usable font file found for {0} (TeX: {1}). "
                 "The font may lack a Type-1 version.")
                .format(psfont.psname, dvifont.texname))

        pdfname = Name('F%d' % self.nextFont)
        self.nextFont += 1
        matplotlib.verbose.report(
            'Assigning font {0} = {1} (dvi)'.format(pdfname, dvifont.texname),
            'debug')
        self.dviFontInfo[dvifont.texname] = Bunch(
            dvifont=dvifont,
            pdfname=pdfname,
            fontfile=psfont.filename,
            basefont=psfont.psname,
            encodingfile=psfont.encoding,
            effects=psfont.effects)
        return pdfname
