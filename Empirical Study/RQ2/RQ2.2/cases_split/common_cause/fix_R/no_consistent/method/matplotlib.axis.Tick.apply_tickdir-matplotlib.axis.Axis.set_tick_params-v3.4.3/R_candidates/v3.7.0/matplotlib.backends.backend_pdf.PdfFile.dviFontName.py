    def dviFontName(self, dvifont):
        """
        Given a dvi font object, return a name suitable for Op.selectfont.
        This registers the font information in ``self.dviFontInfo`` if not yet
        registered.
        """

        dvi_info = self.dviFontInfo.get(dvifont.texname)
        if dvi_info is not None:
            return dvi_info.pdfname

        tex_font_map = dviread.PsfontsMap(dviread._find_tex_file('pdftex.map'))
        psfont = tex_font_map[dvifont.texname]
        if psfont.filename is None:
            raise ValueError(
                "No usable font file found for {} (TeX: {}); "
                "the font may lack a Type-1 version"
                .format(psfont.psname, dvifont.texname))

        pdfname = next(self._internal_font_seq)
        _log.debug('Assigning font %s = %s (dvi)', pdfname, dvifont.texname)
        self.dviFontInfo[dvifont.texname] = types.SimpleNamespace(
            dvifont=dvifont,
            pdfname=pdfname,
            fontfile=psfont.filename,
            basefont=psfont.psname,
            encodingfile=psfont.encoding,
            effects=psfont.effects)
        return pdfname
