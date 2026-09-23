    def _embedTeXFont(self, fontinfo):
        _log.debug('Embedding TeX font %s - fontinfo=%s',
                   fontinfo.dvifont.texname, fontinfo.__dict__)

        # Widths
        widthsObject = self.reserveObject('font widths')
        self.writeObject(widthsObject, fontinfo.dvifont.widths)

        # Font dictionary
        fontdictObject = self.reserveObject('font dictionary')
        fontdict = {
            'Type':      Name('Font'),
            'Subtype':   Name('Type1'),
            'FirstChar': 0,
            'LastChar':  len(fontinfo.dvifont.widths) - 1,
            'Widths':    widthsObject,
            }

        # Encoding (if needed)
        if fontinfo.encodingfile is not None:
            fontdict['Encoding'] = {
                'Type': Name('Encoding'),
                'Differences': [
                    0, *map(Name, dviread._parse_enc(fontinfo.encodingfile))],
            }

        # If no file is specified, stop short
        if fontinfo.fontfile is None:
            _log.warning(
                "Because of TeX configuration (pdftex.map, see updmap option "
                "pdftexDownloadBase14) the font %s is not embedded. This is "
                "deprecated as of PDF 1.5 and it may cause the consumer "
                "application to show something that was not intended.",
                fontinfo.basefont)
            fontdict['BaseFont'] = Name(fontinfo.basefont)
            self.writeObject(fontdictObject, fontdict)
            return fontdictObject

        # We have a font file to embed - read it in and apply any effects
        t1font = type1font.Type1Font(fontinfo.fontfile)
        if fontinfo.effects:
            t1font = t1font.transform(fontinfo.effects)
        fontdict['BaseFont'] = Name(t1font.prop['FontName'])

        # Font descriptors may be shared between differently encoded
        # Type-1 fonts, so only create a new descriptor if there is no
        # existing descriptor for this font.
        effects = (fontinfo.effects.get('slant', 0.0),
                   fontinfo.effects.get('extend', 1.0))
        fontdesc = self.type1Descriptors.get((fontinfo.fontfile, effects))
        if fontdesc is None:
            fontdesc = self.createType1Descriptor(t1font, fontinfo.fontfile)
            self.type1Descriptors[(fontinfo.fontfile, effects)] = fontdesc
        fontdict['FontDescriptor'] = fontdesc

        self.writeObject(fontdictObject, fontdict)
        return fontdictObject
