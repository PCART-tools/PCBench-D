    def embedTTF(self, filename, characters):
        """Embed the TTF font from the named file into the document."""

        font = get_font(filename)
        fonttype = rcParams['pdf.fonttype']

        def cvt(length, upe=font.units_per_EM, nearest=True):
            "Convert font coordinates to PDF glyph coordinates"
            value = length / upe * 1000
            if nearest:
                return round(value)
            # Best(?) to round away from zero for bounding boxes and the like.
            if value < 0:
                return math.floor(value)
            else:
                return math.ceil(value)

        def embedTTFType3(font, characters, descriptor):
            """The Type 3-specific part of embedding a Truetype font"""
            widthsObject = self.reserveObject('font widths')
            fontdescObject = self.reserveObject('font descriptor')
            fontdictObject = self.reserveObject('font dictionary')
            charprocsObject = self.reserveObject('character procs')
            differencesArray = []
            firstchar, lastchar = 0, 255
            bbox = [cvt(x, nearest=False) for x in font.bbox]

            fontdict = {
                'Type': Name('Font'),
                'BaseFont': ps_name,
                'FirstChar': firstchar,
                'LastChar': lastchar,
                'FontDescriptor': fontdescObject,
                'Subtype': Name('Type3'),
                'Name': descriptor['FontName'],
                'FontBBox': bbox,
                'FontMatrix': [.001, 0, 0, .001, 0, 0],
                'CharProcs': charprocsObject,
                'Encoding': {
                    'Type': Name('Encoding'),
                    'Differences': differencesArray},
                'Widths': widthsObject
                }

            from encodings import cp1252

            # Make the "Widths" array
            def get_char_width(charcode):
                s = ord(cp1252.decoding_table[charcode])
                width = font.load_char(
                    s, flags=LOAD_NO_SCALE | LOAD_NO_HINTING).horiAdvance
                return cvt(width)

            with warnings.catch_warnings():
                # Ignore 'Required glyph missing from current font' warning
                # from ft2font: here we're just building the widths table, but
                # the missing glyphs may not even be used in the actual string.
                warnings.filterwarnings("ignore")
                widths = [get_char_width(charcode)
                          for charcode in range(firstchar, lastchar+1)]
            descriptor['MaxWidth'] = max(widths)

            # Make the "Differences" array, sort the ccodes < 255 from
            # the multi-byte ccodes, and build the whole set of glyph ids
            # that we need from this font.
            glyph_ids = []
            differences = []
            multi_byte_chars = set()
            for c in characters:
                ccode = c
                gind = font.get_char_index(ccode)
                glyph_ids.append(gind)
                glyph_name = font.get_glyph_name(gind)
                if ccode <= 255:
                    differences.append((ccode, glyph_name))
                else:
                    multi_byte_chars.add(glyph_name)
            differences.sort()

            last_c = -2
            for c, name in differences:
                if c != last_c + 1:
                    differencesArray.append(c)
                differencesArray.append(Name(name))
                last_c = c

            # Make the charprocs array (using ttconv to generate the
            # actual outlines)
            try:
                rawcharprocs = ttconv.get_pdf_charprocs(
                    os.fsencode(filename), glyph_ids)
            except RuntimeError:
                _log.warning("The PDF backend does not currently support the "
                             "selected font.")
                raise
            charprocs = {}
            for charname in sorted(rawcharprocs):
                stream = rawcharprocs[charname]
                charprocDict = {'Length': len(stream)}
                # The 2-byte characters are used as XObjects, so they
                # need extra info in their dictionary
                if charname in multi_byte_chars:
                    charprocDict['Type'] = Name('XObject')
                    charprocDict['Subtype'] = Name('Form')
                    charprocDict['BBox'] = bbox
                    # Each glyph includes bounding box information,
                    # but xpdf and ghostscript can't handle it in a
                    # Form XObject (they segfault!!!), so we remove it
                    # from the stream here.  It's not needed anyway,
                    # since the Form XObject includes it in its BBox
                    # value.
                    stream = stream[stream.find(b"d1") + 2:]
                charprocObject = self.reserveObject('charProc')
                self.beginStream(charprocObject.id, None, charprocDict)
                self.currentstream.write(stream)
                self.endStream()

                # Send the glyphs with ccode > 255 to the XObject dictionary,
                # and the others to the font itself
                if charname in multi_byte_chars:
                    name = self._get_xobject_symbol_name(filename, charname)
                    self.multi_byte_charprocs[name] = charprocObject
                else:
                    charprocs[charname] = charprocObject

            # Write everything out
            self.writeObject(fontdictObject, fontdict)
            self.writeObject(fontdescObject, descriptor)
            self.writeObject(widthsObject, widths)
            self.writeObject(charprocsObject, charprocs)

            return fontdictObject

        def embedTTFType42(font, characters, descriptor):
            """The Type 42-specific part of embedding a Truetype font"""
            fontdescObject = self.reserveObject('font descriptor')
            cidFontDictObject = self.reserveObject('CID font dictionary')
            type0FontDictObject = self.reserveObject('Type 0 font dictionary')
            cidToGidMapObject = self.reserveObject('CIDToGIDMap stream')
            fontfileObject = self.reserveObject('font file stream')
            wObject = self.reserveObject('Type 0 widths')
            toUnicodeMapObject = self.reserveObject('ToUnicode map')

            cidFontDict = {
                'Type': Name('Font'),
                'Subtype': Name('CIDFontType2'),
                'BaseFont': ps_name,
                'CIDSystemInfo': {
                    'Registry': 'Adobe',
                    'Ordering': 'Identity',
                    'Supplement': 0},
                'FontDescriptor': fontdescObject,
                'W': wObject,
                'CIDToGIDMap': cidToGidMapObject
                }

            type0FontDict = {
                'Type': Name('Font'),
                'Subtype': Name('Type0'),
                'BaseFont': ps_name,
                'Encoding': Name('Identity-H'),
                'DescendantFonts': [cidFontDictObject],
                'ToUnicode': toUnicodeMapObject
                }

            # Make fontfile stream
            descriptor['FontFile2'] = fontfileObject
            length1Object = self.reserveObject('decoded length of a font')
            self.beginStream(
                fontfileObject.id,
                self.reserveObject('length of font stream'),
                {'Length1': length1Object})
            with open(filename, 'rb') as fontfile:
                length1 = 0
                while True:
                    data = fontfile.read(4096)
                    if not data:
                        break
                    length1 += len(data)
                    self.currentstream.write(data)
            self.endStream()
            self.writeObject(length1Object, length1)

            # Make the 'W' (Widths) array, CidToGidMap and ToUnicode CMap
            # at the same time
            cid_to_gid_map = ['\0'] * 65536
            widths = []
            max_ccode = 0
            for c in characters:
                ccode = c
                gind = font.get_char_index(ccode)
                glyph = font.load_char(ccode,
                                       flags=LOAD_NO_SCALE | LOAD_NO_HINTING)
                widths.append((ccode, cvt(glyph.horiAdvance)))
                if ccode < 65536:
                    cid_to_gid_map[ccode] = chr(gind)
                max_ccode = max(ccode, max_ccode)
            widths.sort()
            cid_to_gid_map = cid_to_gid_map[:max_ccode + 1]

            last_ccode = -2
            w = []
            max_width = 0
            unicode_groups = []
            for ccode, width in widths:
                if ccode != last_ccode + 1:
                    w.append(ccode)
                    w.append([width])
                    unicode_groups.append([ccode, ccode])
                else:
                    w[-1].append(width)
                    unicode_groups[-1][1] = ccode
                max_width = max(max_width, width)
                last_ccode = ccode

            unicode_bfrange = []
            for start, end in unicode_groups:
                unicode_bfrange.append(
                    b"<%04x> <%04x> [%s]" %
                    (start, end,
                     b" ".join(b"<%04x>" % x for x in range(start, end+1))))
            unicode_cmap = (self._identityToUnicodeCMap %
                            (len(unicode_groups), b"\n".join(unicode_bfrange)))

            # CIDToGIDMap stream
            cid_to_gid_map = "".join(cid_to_gid_map).encode("utf-16be")
            self.beginStream(cidToGidMapObject.id,
                             None,
                             {'Length': len(cid_to_gid_map)})
            self.currentstream.write(cid_to_gid_map)
            self.endStream()

            # ToUnicode CMap
            self.beginStream(toUnicodeMapObject.id,
                             None,
                             {'Length': unicode_cmap})
            self.currentstream.write(unicode_cmap)
            self.endStream()

            descriptor['MaxWidth'] = max_width

            # Write everything out
            self.writeObject(cidFontDictObject, cidFontDict)
            self.writeObject(type0FontDictObject, type0FontDict)
            self.writeObject(fontdescObject, descriptor)
            self.writeObject(wObject, w)

            return type0FontDictObject

        # Beginning of main embedTTF function...

        ps_name = font.postscript_name.encode('ascii', 'replace')
        ps_name = Name(ps_name)
        pclt = font.get_sfnt_table('pclt') or {'capHeight': 0, 'xHeight': 0}
        post = font.get_sfnt_table('post') or {'italicAngle': (0, 0)}
        ff = font.face_flags
        sf = font.style_flags

        flags = 0
        symbolic = False  # ps_name.name in ('Cmsy10', 'Cmmi10', 'Cmex10')
        if ff & FIXED_WIDTH:
            flags |= 1 << 0
        if 0:  # TODO: serif
            flags |= 1 << 1
        if symbolic:
            flags |= 1 << 2
        else:
            flags |= 1 << 5
        if sf & ITALIC:
            flags |= 1 << 6
        if 0:  # TODO: all caps
            flags |= 1 << 16
        if 0:  # TODO: small caps
            flags |= 1 << 17
        if 0:  # TODO: force bold
            flags |= 1 << 18

        descriptor = {
            'Type': Name('FontDescriptor'),
            'FontName': ps_name,
            'Flags': flags,
            'FontBBox': [cvt(x, nearest=False) for x in font.bbox],
            'Ascent': cvt(font.ascender, nearest=False),
            'Descent': cvt(font.descender, nearest=False),
            'CapHeight': cvt(pclt['capHeight'], nearest=False),
            'XHeight': cvt(pclt['xHeight']),
            'ItalicAngle': post['italicAngle'][1],  # ???
            'StemV': 0  # ???
            }

        # The font subsetting to a Type 3 font does not work for
        # OpenType (.otf) that embed a Postscript CFF font, so avoid that --
        # save as a (non-subsetted) Type 42 font instead.
        if is_opentype_cff_font(filename):
            fonttype = 42
            _log.warning("%r can not be subsetted into a Type 3 font. The "
                         "entire font will be embedded in the output.",
                         os.path.basename(filename))

        if fonttype == 3:
            return embedTTFType3(font, characters, descriptor)
        elif fonttype == 42:
            return embedTTFType42(font, characters, descriptor)
