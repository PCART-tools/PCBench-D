class PdfFile(object):
    """PDF file object."""

    def __init__(self, filename, metadata=None):
        self.nextObject = 1     # next free object id
        self.xrefTable = [[0, 65535, 'the zero object']]
        self.passed_in_file_object = False
        self.original_file_like = None
        self.tell_base = 0
        fh, opened = cbook.to_filehandle(filename, "wb", return_opened=True)
        if not opened:
            try:
                self.tell_base = filename.tell()
            except IOError:
                fh = BytesIO()
                self.original_file_like = filename
            else:
                fh = filename
                self.passed_in_file_object = True

        self._core14fontdir = os.path.join(
            rcParams['datapath'], 'fonts', 'pdfcorefonts')
        self.fh = fh
        self.currentstream = None  # stream object to write to, if any
        fh.write(b"%PDF-1.4\n")    # 1.4 is the first version to have alpha
        # Output some eight-bit chars as a comment so various utilities
        # recognize the file as binary by looking at the first few
        # lines (see note in section 3.4.1 of the PDF reference).
        fh.write(b"%\254\334 \253\272\n")

        self.rootObject = self.reserveObject('root')
        self.pagesObject = self.reserveObject('pages')
        self.pageList = []
        self.fontObject = self.reserveObject('fonts')
        self.alphaStateObject = self.reserveObject('extended graphics states')
        self.hatchObject = self.reserveObject('tiling patterns')
        self.gouraudObject = self.reserveObject('Gouraud triangles')
        self.XObjectObject = self.reserveObject('external objects')
        self.resourceObject = self.reserveObject('resources')

        root = {'Type': Name('Catalog'),
                'Pages': self.pagesObject}
        self.writeObject(self.rootObject, root)

        # get source date from SOURCE_DATE_EPOCH, if set
        # See https://reproducible-builds.org/specs/source-date-epoch/
        source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
        if source_date_epoch:
            source_date = datetime.utcfromtimestamp(int(source_date_epoch))
            source_date = source_date.replace(tzinfo=UTC)
        else:
            source_date = datetime.today()

        self.infoDict = {
            'Creator': 'matplotlib %s, http://matplotlib.org' % __version__,
            'Producer': 'matplotlib pdf backend %s' % __version__,
            'CreationDate': source_date
        }
        if metadata is not None:
            self.infoDict.update(metadata)
        self.infoDict = {k: v for (k, v) in self.infoDict.items()
                         if v is not None}

        self.fontNames = {}     # maps filenames to internal font names
        self.nextFont = 1       # next free internal font name
        self.dviFontInfo = {}   # maps dvi font names to embedding information
        self._texFontMap = None  # maps TeX font names to PostScript fonts
        # differently encoded Type-1 fonts may share the same descriptor
        self.type1Descriptors = {}
        self.used_characters = {}

        self.alphaStates = {}   # maps alpha values to graphics state objects
        self.nextAlphaState = 1
        # reproducible writeHatches needs an ordered dict:
        self.hatchPatterns = collections.OrderedDict()
        self.nextHatch = 1
        self.gouraudTriangles = []

        self._images = collections.OrderedDict()   # reproducible writeImages
        self.nextImage = 1

        self.markers = collections.OrderedDict()   # reproducible writeMarkers
        self.multi_byte_charprocs = {}

        self.paths = []

        self.pageAnnotations = []  # A list of annotations for the
                                   # current page

        # The PDF spec recommends to include every procset
        procsets = [Name(x)
                    for x in "PDF Text ImageB ImageC ImageI".split()]

        # Write resource dictionary.
        # Possibly TODO: more general ExtGState (graphics state dictionaries)
        #                ColorSpace Pattern Shading Properties
        resources = {'Font': self.fontObject,
                     'XObject': self.XObjectObject,
                     'ExtGState': self.alphaStateObject,
                     'Pattern': self.hatchObject,
                     'Shading': self.gouraudObject,
                     'ProcSet': procsets}
        self.writeObject(self.resourceObject, resources)

    def newPage(self, width, height):
        self.endStream()

        self.width, self.height = width, height
        contentObject = self.reserveObject('page contents')
        thePage = {'Type': Name('Page'),
                   'Parent': self.pagesObject,
                   'Resources': self.resourceObject,
                   'MediaBox': [0, 0, 72 * width, 72 * height],
                   'Contents': contentObject,
                   'Group': {'Type': Name('Group'),
                             'S': Name('Transparency'),
                             'CS': Name('DeviceRGB')},
                   'Annots': self.pageAnnotations,
                   }
        pageObject = self.reserveObject('page')
        self.writeObject(pageObject, thePage)
        self.pageList.append(pageObject)

        self.beginStream(contentObject.id,
                         self.reserveObject('length of content stream'))
        # Initialize the pdf graphics state to match the default mpl
        # graphics context: currently only the join style needs to be set
        self.output(GraphicsContextPdf.joinstyles['round'], Op.setlinejoin)

        # Clear the list of annotations for the next page
        self.pageAnnotations = []

    def newTextnote(self, text, positionRect=[-100, -100, 0, 0]):
        # Create a new annotation of type text
        theNote = {'Type': Name('Annot'),
                   'Subtype': Name('Text'),
                   'Contents': text,
                   'Rect': positionRect,
                   }
        annotObject = self.reserveObject('annotation')
        self.writeObject(annotObject, theNote)
        self.pageAnnotations.append(annotObject)

    def finalize(self):
        "Write out the various deferred objects and the pdf end matter."

        self.endStream()
        self.writeFonts()
        self.writeObject(
            self.alphaStateObject,
            {val[0]: val[1] for val in self.alphaStates.values()})
        self.writeHatches()
        self.writeGouraudTriangles()
        xobjects = {
            name: ob for image, name, ob in self._images.values()}
        for tup in self.markers.values():
            xobjects[tup[0]] = tup[1]
        for name, value in self.multi_byte_charprocs.items():
            xobjects[name] = value
        for name, path, trans, ob, join, cap, padding, filled, stroked \
                in self.paths:
            xobjects[name] = ob
        self.writeObject(self.XObjectObject, xobjects)
        self.writeImages()
        self.writeMarkers()
        self.writePathCollectionTemplates()
        self.writeObject(self.pagesObject,
                         {'Type': Name('Pages'),
                          'Kids': self.pageList,
                          'Count': len(self.pageList)})
        self.writeInfoDict()

        # Finalize the file
        self.writeXref()
        self.writeTrailer()

    def close(self):
        "Flush all buffers and free all resources."

        self.endStream()
        if self.passed_in_file_object:
            self.fh.flush()
        else:
            if self.original_file_like is not None:
                self.original_file_like.write(self.fh.getvalue())
            self.fh.close()

    def write(self, data):
        if self.currentstream is None:
            self.fh.write(data)
        else:
            self.currentstream.write(data)

    def output(self, *data):
        self.write(fill([pdfRepr(x) for x in data]))
        self.write(b'\n')

    def beginStream(self, id, len, extra=None, png=None):
        assert self.currentstream is None
        self.currentstream = Stream(id, len, self, extra, png)

    def endStream(self):
        if self.currentstream is not None:
            self.currentstream.end()
            self.currentstream = None

    def fontName(self, fontprop):
        """
        Select a font based on fontprop and return a name suitable for
        Op.selectfont. If fontprop is a string, it will be interpreted
        as the filename of the font.
        """

        if isinstance(fontprop, str):
            filename = fontprop
        elif rcParams['pdf.use14corefonts']:
            filename = findfont(
                fontprop, fontext='afm', directory=self._core14fontdir)
            if filename is None:
                filename = findfont(
                    "Helvetica", fontext='afm', directory=self._core14fontdir)
        else:
            filename = findfont(fontprop)

        Fx = self.fontNames.get(filename)
        if Fx is None:
            Fx = Name('F%d' % self.nextFont)
            self.fontNames[filename] = Fx
            self.nextFont += 1
            _log.debug('Assigning font %s = %r', Fx, filename)

        return Fx

    @property
    @cbook.deprecated("3.0")
    def texFontMap(self):
        # lazy-load texFontMap, it takes a while to parse
        # and usetex is a relatively rare use case
        return dviread.PsfontsMap(dviread.find_tex_file('pdftex.map'))

    def dviFontName(self, dvifont):
        """
        Given a dvi font object, return a name suitable for Op.selectfont.
        This registers the font information in self.dviFontInfo if not yet
        registered.
        """

        dvi_info = self.dviFontInfo.get(dvifont.texname)
        if dvi_info is not None:
            return dvi_info.pdfname

        tex_font_map = dviread.PsfontsMap(dviread.find_tex_file('pdftex.map'))
        psfont = tex_font_map[dvifont.texname]
        if psfont.filename is None:
            raise ValueError(
                "No usable font file found for {} (TeX: {}); "
                "the font may lack a Type-1 version"
                .format(psfont.psname, dvifont.texname))

        pdfname = Name('F%d' % self.nextFont)
        self.nextFont += 1
        _log.debug('Assigning font %s = %s (dvi)', pdfname, dvifont.texname)
        self.dviFontInfo[dvifont.texname] = types.SimpleNamespace(
            dvifont=dvifont,
            pdfname=pdfname,
            fontfile=psfont.filename,
            basefont=psfont.psname,
            encodingfile=psfont.encoding,
            effects=psfont.effects)
        return pdfname

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
                realpath, stat_key = get_realpath_and_stat(filename)
                chars = self.used_characters.get(stat_key)
                if chars is not None and len(chars[1]):
                    fonts[Fx] = self.embedTTF(realpath, chars[1])
        self.writeObject(self.fontObject, fonts)

    def _write_afm_font(self, filename):
        with open(filename, 'rb') as fh:
            font = AFM(fh)
        fontname = font.get_fontname()
        fontdict = {'Type': Name('Font'),
                    'Subtype': Name('Type1'),
                    'BaseFont': Name(fontname),
                    'Encoding': Name('WinAnsiEncoding')}
        fontdictObject = self.reserveObject('font dictionary')
        self.writeObject(fontdictObject, fontdict)
        return fontdictObject

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
            enc = dviread.Encoding(fontinfo.encodingfile)
            differencesArray = [Name(ch) for ch in enc]
            differencesArray = [0] + differencesArray
            fontdict['Encoding'] = \
                {'Type': Name('Encoding'),
                 'Differences': differencesArray}

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

        self.beginStream(fontfileObject.id, None,
                         {'Length1': len(t1font.parts[0]),
                          'Length2': len(t1font.parts[1]),
                          'Length3': 0})
        self.currentstream.write(t1font.parts[0])
        self.currentstream.write(t1font.parts[1])
        self.endStream()

        return fontdescObject

    def _get_xobject_symbol_name(self, filename, symbol_name):
        return "%s-%s" % (
            os.path.splitext(os.path.basename(filename))[0],
            symbol_name)

    _identityToUnicodeCMap = b"""/CIDInit /ProcSet findresource begin
12 dict begin
begincmap
/CIDSystemInfo
<< /Registry (Adobe)
   /Ordering (UCS)
   /Supplement 0
>> def
/CMapName /Adobe-Identity-UCS def
/CMapType 2 def
1 begincodespacerange
<0000> <ffff>
endcodespacerange
%d beginbfrange
%s
endbfrange
endcmap
CMapName currentdict /CMap defineresource pop
end
end"""

    def embedTTF(self, filename, characters):
        """Embed the TTF font from the named file into the document."""

        font = get_font(filename)
        fonttype = rcParams['pdf.fonttype']

        def cvt(length, upe=font.units_per_EM, nearest=True):
            "Convert font coordinates to PDF glyph coordinates"
            value = length / upe * 1000
            if nearest:
                return np.round(value)
            # Perhaps best to round away from zero for bounding
            # boxes and the like
            if value < 0:
                return floor(value)
            else:
                return ceil(value)

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

            # Make the "Widths" array
            from encodings import cp1252
            # The "decoding_map" was changed
            # to a "decoding_table" as of Python 2.5.
            if hasattr(cp1252, 'decoding_map'):
                def decode_char(charcode):
                    return cp1252.decoding_map[charcode] or 0
            else:
                def decode_char(charcode):
                    return ord(cp1252.decoding_table[charcode])

            def get_char_width(charcode):
                s = decode_char(charcode)
                width = font.load_char(
                    s, flags=LOAD_NO_SCALE | LOAD_NO_HINTING).horiAdvance
                return cvt(width)

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
            rawcharprocs = ttconv.get_pdf_charprocs(
                os.fsencode(filename), glyph_ids)
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

    def alphaState(self, alpha):
        """Return name of an ExtGState that sets alpha to the given value."""

        state = self.alphaStates.get(alpha, None)
        if state is not None:
            return state[0]

        name = Name('A%d' % self.nextAlphaState)
        self.nextAlphaState += 1
        self.alphaStates[alpha] = \
            (name, {'Type': Name('ExtGState'),
                    'CA': alpha[0], 'ca': alpha[1]})
        return name

    def hatchPattern(self, hatch_style):
        # The colors may come in as numpy arrays, which aren't hashable
        if hatch_style is not None:
            edge, face, hatch = hatch_style
            if edge is not None:
                edge = tuple(edge)
            if face is not None:
                face = tuple(face)
            hatch_style = (edge, face, hatch)

        pattern = self.hatchPatterns.get(hatch_style, None)
        if pattern is not None:
            return pattern

        name = Name('H%d' % self.nextHatch)
        self.nextHatch += 1
        self.hatchPatterns[hatch_style] = name
        return name

    def writeHatches(self):
        hatchDict = dict()
        sidelen = 72.0
        for hatch_style, name in self.hatchPatterns.items():
            ob = self.reserveObject('hatch pattern')
            hatchDict[name] = ob
            res = {'Procsets':
                   [Name(x) for x in "PDF Text ImageB ImageC ImageI".split()]}
            self.beginStream(
                ob.id, None,
                {'Type': Name('Pattern'),
                 'PatternType': 1, 'PaintType': 1, 'TilingType': 1,
                 'BBox': [0, 0, sidelen, sidelen],
                 'XStep': sidelen, 'YStep': sidelen,
                 'Resources': res,
                 # Change origin to match Agg at top-left.
                 'Matrix': [1, 0, 0, 1, 0, self.height * 72]})

            stroke_rgb, fill_rgb, path = hatch_style
            self.output(stroke_rgb[0], stroke_rgb[1], stroke_rgb[2],
                        Op.setrgb_stroke)
            if fill_rgb is not None:
                self.output(fill_rgb[0], fill_rgb[1], fill_rgb[2],
                            Op.setrgb_nonstroke,
                            0, 0, sidelen, sidelen, Op.rectangle,
                            Op.fill)

            self.output(rcParams['hatch.linewidth'], Op.setlinewidth)

            self.output(*self.pathOperations(
                Path.hatch(path),
                Affine2D().scale(sidelen),
                simplify=False))
            self.output(Op.fill_stroke)

            self.endStream()
        self.writeObject(self.hatchObject, hatchDict)

    def addGouraudTriangles(self, points, colors):
        name = Name('GT%d' % len(self.gouraudTriangles))
        self.gouraudTriangles.append((name, points, colors))
        return name

    def writeGouraudTriangles(self):
        gouraudDict = dict()
        for name, points, colors in self.gouraudTriangles:
            ob = self.reserveObject('Gouraud triangle')
            gouraudDict[name] = ob
            shape = points.shape
            flat_points = points.reshape((shape[0] * shape[1], 2))
            flat_colors = colors.reshape((shape[0] * shape[1], 4))
            points_min = np.min(flat_points, axis=0) - (1 << 8)
            points_max = np.max(flat_points, axis=0) + (1 << 8)
            factor = 0xffffffff / (points_max - points_min)

            self.beginStream(
                ob.id, None,
                {'ShadingType': 4,
                 'BitsPerCoordinate': 32,
                 'BitsPerComponent': 8,
                 'BitsPerFlag': 8,
                 'ColorSpace': Name('DeviceRGB'),
                 'AntiAlias': True,
                 'Decode': [points_min[0], points_max[0],
                            points_min[1], points_max[1],
                            0, 1, 0, 1, 0, 1]
                 })

            streamarr = np.empty(
                (shape[0] * shape[1],),
                dtype=[('flags', 'u1'),
                       ('points', '>u4', (2,)),
                       ('colors', 'u1', (3,))])
            streamarr['flags'] = 0
            streamarr['points'] = (flat_points - points_min) * factor
            streamarr['colors'] = flat_colors[:, :3] * 255.0

            self.write(streamarr.tostring())
            self.endStream()
        self.writeObject(self.gouraudObject, gouraudDict)

    def imageObject(self, image):
        """Return name of an image XObject representing the given image."""

        entry = self._images.get(id(image), None)
        if entry is not None:
            return entry[1]

        name = Name('I%d' % self.nextImage)
        ob = self.reserveObject('image %d' % self.nextImage)
        self.nextImage += 1
        self._images[id(image)] = (image, name, ob)
        return name

    def _unpack(self, im):
        """
        Unpack the image object im into height, width, data, alpha,
        where data and alpha are HxWx3 (RGB) or HxWx1 (grayscale or alpha)
        arrays, except alpha is None if the image is fully opaque.
        """
        h, w = im.shape[:2]
        im = im[::-1]
        if im.ndim == 2:
            return h, w, im, None
        else:
            rgb = im[:, :, :3]
            rgb = np.array(rgb, order='C')
            # PDF needs a separate alpha image
            if im.shape[2] == 4:
                alpha = im[:, :, 3][..., None]
                if np.all(alpha == 255):
                    alpha = None
                else:
                    alpha = np.array(alpha, order='C')
            else:
                alpha = None
            return h, w, rgb, alpha

    def _writePng(self, data):
        """
        Write the image *data* into the pdf file using png
        predictors with Flate compression.
        """

        buffer = BytesIO()
        _png.write_png(data, buffer)
        buffer.seek(8)
        written = 0
        header = bytearray(8)
        while True:
            n = buffer.readinto(header)
            assert n == 8
            length, type = struct.unpack(b'!L4s', bytes(header))
            if type == b'IDAT':
                data = bytearray(length)
                n = buffer.readinto(data)
                assert n == length
                self.currentstream.write(bytes(data))
                written += n
            elif type == b'IEND':
                break
            else:
                buffer.seek(length, 1)
            buffer.seek(4, 1)   # skip CRC

    def _writeImg(self, data, height, width, grayscale, id, smask=None):
        """
        Write the image *data* of size *height* x *width*, as grayscale
        if *grayscale* is true and RGB otherwise, as pdf object *id*
        and with the soft mask (alpha channel) *smask*, which should be
        either None or a *height* x *width* x 1 array.
        """

        obj = {'Type':             Name('XObject'),
               'Subtype':          Name('Image'),
               'Width':            width,
               'Height':           height,
               'ColorSpace':       Name('DeviceGray' if grayscale
                                        else 'DeviceRGB'),
               'BitsPerComponent': 8}
        if smask:
            obj['SMask'] = smask
        if rcParams['pdf.compression']:
            png = {'Predictor': 10,
                   'Colors':    1 if grayscale else 3,
                   'Columns':   width}
        else:
            png = None
        self.beginStream(
            id,
            self.reserveObject('length of image stream'),
            obj,
            png=png
            )
        if png:
            self._writePng(data)
        else:
            self.currentstream.write(data.tostring())
        self.endStream()

    def writeImages(self):
        for img, name, ob in self._images.values():
            height, width, data, adata = self._unpack(img)
            if adata is not None:
                smaskObject = self.reserveObject("smask")
                self._writeImg(adata, height, width, True, smaskObject.id)
            else:
                smaskObject = None
            self._writeImg(data, height, width, False,
                           ob.id, smaskObject)

    def markerObject(self, path, trans, fill, stroke, lw, joinstyle,
                     capstyle):
        """Return name of a marker XObject representing the given path."""
        # self.markers used by markerObject, writeMarkers, close:
        # mapping from (path operations, fill?, stroke?) to
        #   [name, object reference, bounding box, linewidth]
        # This enables different draw_markers calls to share the XObject
        # if the gc is sufficiently similar: colors etc can vary, but
        # the choices of whether to fill and whether to stroke cannot.
        # We need a bounding box enclosing all of the XObject path,
        # but since line width may vary, we store the maximum of all
        # occurring line widths in self.markers.
        # close() is somewhat tightly coupled in that it expects the
        # first two components of each value in self.markers to be the
        # name and object reference.
        pathops = self.pathOperations(path, trans, simplify=False)
        key = (tuple(pathops), bool(fill), bool(stroke), joinstyle, capstyle)
        result = self.markers.get(key)
        if result is None:
            name = Name('M%d' % len(self.markers))
            ob = self.reserveObject('marker %d' % len(self.markers))
            bbox = path.get_extents(trans)
            self.markers[key] = [name, ob, bbox, lw]
        else:
            if result[-1] < lw:
                result[-1] = lw
            name = result[0]
        return name

    def writeMarkers(self):
        for ((pathops, fill, stroke, joinstyle, capstyle),
             (name, ob, bbox, lw)) in self.markers.items():
            bbox = bbox.padded(lw * 0.5)
            self.beginStream(
                ob.id, None,
                {'Type': Name('XObject'), 'Subtype': Name('Form'),
                 'BBox': list(bbox.extents)})
            self.output(GraphicsContextPdf.joinstyles[joinstyle],
                        Op.setlinejoin)
            self.output(GraphicsContextPdf.capstyles[capstyle], Op.setlinecap)
            self.output(*pathops)
            self.output(Op.paint_path(fill, stroke))
            self.endStream()

    def pathCollectionObject(self, gc, path, trans, padding, filled, stroked):
        name = Name('P%d' % len(self.paths))
        ob = self.reserveObject('path %d' % len(self.paths))
        self.paths.append(
            (name, path, trans, ob, gc.get_joinstyle(), gc.get_capstyle(),
             padding, filled, stroked))
        return name

    def writePathCollectionTemplates(self):
        for (name, path, trans, ob, joinstyle, capstyle, padding, filled,
             stroked) in self.paths:
            pathops = self.pathOperations(path, trans, simplify=False)
            bbox = path.get_extents(trans)
            if not np.all(np.isfinite(bbox.extents)):
                extents = [0, 0, 0, 0]
            else:
                bbox = bbox.padded(padding)
                extents = list(bbox.extents)
            self.beginStream(
                ob.id, None,
                {'Type': Name('XObject'), 'Subtype': Name('Form'),
                 'BBox': extents})
            self.output(GraphicsContextPdf.joinstyles[joinstyle],
                        Op.setlinejoin)
            self.output(GraphicsContextPdf.capstyles[capstyle], Op.setlinecap)
            self.output(*pathops)
            self.output(Op.paint_path(filled, stroked))
            self.endStream()

    @staticmethod
    def pathOperations(path, transform, clip=None, simplify=None, sketch=None):
        return [Verbatim(_path.convert_to_string(
            path, transform, clip, simplify, sketch,
            6,
            [Op.moveto.op, Op.lineto.op, b'', Op.curveto.op, Op.closepath.op],
            True))]

    def writePath(self, path, transform, clip=False, sketch=None):
        if clip:
            clip = (0.0, 0.0, self.width * 72, self.height * 72)
            simplify = path.should_simplify
        else:
            clip = None
            simplify = False
        cmds = self.pathOperations(path, transform, clip, simplify=simplify,
                                   sketch=sketch)
        self.output(*cmds)

    def reserveObject(self, name=''):
        """Reserve an ID for an indirect object.
        The name is used for debugging in case we forget to print out
        the object with writeObject.
        """

        id = self.nextObject
        self.nextObject += 1
        self.xrefTable.append([None, 0, name])
        return Reference(id)

    def recordXref(self, id):
        self.xrefTable[id][0] = self.fh.tell() - self.tell_base

    def writeObject(self, object, contents):
        self.recordXref(object.id)
        object.write(contents, self)

    def writeXref(self):
        """Write out the xref table."""

        self.startxref = self.fh.tell() - self.tell_base
        self.write(b"xref\n0 %d\n" % self.nextObject)
        i = 0
        borken = False
        for offset, generation, name in self.xrefTable:
            if offset is None:
                print('No offset for object %d (%s)' % (i, name),
                      file=sys.stderr)
                borken = True
            else:
                key = b"f" if name == 'the zero object' else b"n"
                text = b"%010d %05d %b \n" % (offset, generation, key)
                self.write(text)
            i += 1
        if borken:
            raise AssertionError('Indirect object does not exist')

    def writeInfoDict(self):
        """Write out the info dictionary, checking it for good form"""

        def is_string_like(x):
            return isinstance(x, str)

        def is_date(x):
            return isinstance(x, datetime)

        check_trapped = (lambda x: isinstance(x, Name) and
                         x.name in ('True', 'False', 'Unknown'))

        keywords = {'Title': is_string_like,
                    'Author': is_string_like,
                    'Subject': is_string_like,
                    'Keywords': is_string_like,
                    'Creator': is_string_like,
                    'Producer': is_string_like,
                    'CreationDate': is_date,
                    'ModDate': is_date,
                    'Trapped': check_trapped}
        for k in self.infoDict:
            if k not in keywords:
                warnings.warn('Unknown infodict keyword: %s' % k, stacklevel=2)
            else:
                if not keywords[k](self.infoDict[k]):
                    warnings.warn('Bad value for infodict keyword %s' % k,
                                  stacklevel=2)

        self.infoObject = self.reserveObject('info')
        self.writeObject(self.infoObject, self.infoDict)

    def writeTrailer(self):
        """Write out the PDF trailer."""

        self.write(b"trailer\n")
        self.write(pdfRepr(
            {'Size': self.nextObject,
             'Root': self.rootObject,
             'Info': self.infoObject}))
        # Could add 'ID'
        self.write(b"\nstartxref\n%d\n%%%%EOF\n" % self.startxref)
