    def createType1Descriptor(self, t1font, fontfile):
        # Create and write the font descriptor and the font file
        # of a Type-1 font
        fontdescObject = self.reserveObject('font descriptor')
        fontfileObject = self.reserveObject('font file')

        italic_angle = t1font.prop['ItalicAngle']
        fixed_pitch = t1font.prop['isFixedPitch']

        flags = 0
        # fixed width
        if fixed_pitch:
            flags |= 1 << 0
        # TODO: serif
        if 0:
            flags |= 1 << 1
        # TODO: symbolic (most TeX fonts are)
        if 1:
            flags |= 1 << 2
        # non-symbolic
        else:
            flags |= 1 << 5
        # italic
        if italic_angle:
            flags |= 1 << 6
        # TODO: all caps
        if 0:
            flags |= 1 << 16
        # TODO: small caps
        if 0:
            flags |= 1 << 17
        # TODO: force bold
        if 0:
            flags |= 1 << 18

        ft2font = get_font(fontfile)

        descriptor = {
            'Type':        Name('FontDescriptor'),
            'FontName':    Name(t1font.prop['FontName']),
            'Flags':       flags,
            'FontBBox':    ft2font.bbox,
            'ItalicAngle': italic_angle,
            'Ascent':      ft2font.ascender,
            'Descent':     ft2font.descender,
            'CapHeight':   1000,  # TODO: find this out
            'XHeight':     500,  # TODO: this one too
            'FontFile':    fontfileObject,
            'FontFamily':  t1font.prop['FamilyName'],
            'StemV':       50,  # TODO
            # (see also revision 3874; but not all TeX distros have AFM files!)
            # 'FontWeight': a number where 400 = Regular, 700 = Bold
            }

        self.writeObject(fontdescObject, descriptor)

        self.outputStream(fontfileObject, b"".join(t1font.parts[:2]),
                          extra={'Length1': len(t1font.parts[0]),
                                 'Length2': len(t1font.parts[1]),
                                 'Length3': 0})

        return fontdescObject
