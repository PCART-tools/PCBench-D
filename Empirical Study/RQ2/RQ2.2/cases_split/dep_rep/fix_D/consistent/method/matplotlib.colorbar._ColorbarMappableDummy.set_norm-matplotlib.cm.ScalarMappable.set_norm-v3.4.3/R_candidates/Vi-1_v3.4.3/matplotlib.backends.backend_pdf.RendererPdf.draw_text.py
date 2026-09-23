    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        # TODO: combine consecutive texts into one BT/ET delimited section

        self.check_gc(gc, gc._rgb)
        if ismath:
            return self.draw_mathtext(gc, x, y, s, prop, angle)

        fontsize = prop.get_size_in_points()

        if mpl.rcParams['pdf.use14corefonts']:
            font = self._get_font_afm(prop)
            fonttype = 1
        else:
            font = self._get_font_ttf(prop)
            self.file._character_tracker.track(font, s)
            fonttype = mpl.rcParams['pdf.fonttype']

        if gc.get_url() is not None:
            font.set_text(s)
            width, height = font.get_width_height()
            link_annotation = {
                'Type': Name('Annot'),
                'Subtype': Name('Link'),
                'Rect': (x, y, x + width / 64, y + height / 64),
                'Border': [0, 0, 0],
                'A': {
                    'S': Name('URI'),
                    'URI': gc.get_url(),
                },
            }
            self.file._annotations[-1][1].append(link_annotation)

        # If fonttype != 3 emit the whole string at once without manual
        # kerning.
        if fonttype != 3:
            self.file.output(Op.begin_text,
                             self.file.fontName(prop), fontsize, Op.selectfont)
            self._setup_textpos(x, y, angle)
            self.file.output(self.encode_string(s, fonttype),
                             Op.show, Op.end_text)

        # There is no way to access multibyte characters of Type 3 fonts, as
        # they cannot have a CIDMap.  Therefore, in this case we break the
        # string into chunks, where each chunk contains either a string of
        # consecutive 1-byte characters or a single multibyte character.
        # A sequence of 1-byte characters is broken into multiple chunks to
        # adjust the kerning between adjacent chunks.  Each chunk is emitted
        # with a separate command: 1-byte characters use the regular text show
        # command (TJ) with appropriate kerning between chunks, whereas
        # multibyte characters use the XObject command (Do).  (If using Type
        # 42 fonts, all of this complication is avoided, but of course,
        # subsetting those fonts is complex/hard to implement.)
        else:
            # List of (start_x, [prev_kern, char, char, ...]), w/o zero kerns.
            singlebyte_chunks = []
            # List of (start_x, glyph_index).
            multibyte_glyphs = []
            prev_was_multibyte = True
            for item in _text_layout.layout(
                    s, font, kern_mode=KERNING_UNFITTED):
                if ord(item.char) <= 255:
                    if prev_was_multibyte:
                        singlebyte_chunks.append((item.x, []))
                    if item.prev_kern:
                        singlebyte_chunks[-1][1].append(item.prev_kern)
                    singlebyte_chunks[-1][1].append(item.char)
                    prev_was_multibyte = False
                else:
                    multibyte_glyphs.append((item.x, item.glyph_idx))
                    prev_was_multibyte = True
            # Do the rotation and global translation as a single matrix
            # concatenation up front
            self.file.output(Op.gsave)
            a = math.radians(angle)
            self.file.output(math.cos(a), math.sin(a),
                             -math.sin(a), math.cos(a),
                             x, y, Op.concat_matrix)
            # Emit all the 1-byte characters in a BT/ET group.
            self.file.output(Op.begin_text,
                             self.file.fontName(prop), fontsize, Op.selectfont)
            prev_start_x = 0
            for start_x, kerns_or_chars in singlebyte_chunks:
                self._setup_textpos(start_x, 0, 0, prev_start_x, 0, 0)
                self.file.output(
                    # See pdf spec "Text space details" for the 1000/fontsize
                    # (aka. 1000/T_fs) factor.
                    [-1000 * next(group) / fontsize if tp == float  # a kern
                     else self.encode_string("".join(group), fonttype)
                     for tp, group in itertools.groupby(kerns_or_chars, type)],
                    Op.showkern)
                prev_start_x = start_x
            self.file.output(Op.end_text)
            # Then emit all the multibyte characters, one at a time.
            for start_x, glyph_idx in multibyte_glyphs:
                self._draw_xobject_glyph(font, fontsize, glyph_idx, start_x, 0)
            self.file.output(Op.grestore)
