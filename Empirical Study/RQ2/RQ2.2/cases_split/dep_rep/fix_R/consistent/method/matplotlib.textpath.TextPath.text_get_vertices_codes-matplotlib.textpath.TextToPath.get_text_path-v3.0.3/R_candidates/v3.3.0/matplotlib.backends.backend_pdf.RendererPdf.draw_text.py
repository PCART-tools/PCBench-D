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
            # We can't subset all OpenType fonts, so switch to Type 42
            # in that case.
            if is_opentype_cff_font(font.fname):
                fonttype = 42

        # If fonttype != 3 or there are no multibyte characters, emit the whole
        # string at once.
        if fonttype != 3 or all(ord(char) <= 255 for char in s):
            self.file.output(Op.begin_text,
                             self.file.fontName(prop), fontsize, Op.selectfont)
            self._setup_textpos(x, y, angle)
            self.file.output(self.encode_string(s, fonttype), Op.show,
                             Op.end_text)

        # There is no way to access multibyte characters of Type 3 fonts, as
        # they cannot have a CIDMap.  Therefore, in this case we break the
        # string into chunks, where each chunk contains either a string of
        # consecutive 1-byte characters or a single multibyte character.  Each
        # chunk is emitted with a separate command: 1-byte characters use the
        # regular text show command (Tj), whereas multibyte characters use
        # the XObject command (Do).  (If using Type 42 fonts, all of this
        # complication is avoided, but of course, those fonts can not be
        # subsetted.)
        else:
            singlebyte_chunks = []  # List of (start_x, list-of-1-byte-chars).
            multibyte_glyphs = []  # List of (start_x, glyph_index).
            prev_was_singlebyte = False
            for char, (glyph_idx, glyph_x) in zip(
                    s,
                    _text_layout.layout(s, font, kern_mode=KERNING_UNFITTED)):
                if ord(char) <= 255:
                    if prev_was_singlebyte:
                        singlebyte_chunks[-1][1].append(char)
                    else:
                        singlebyte_chunks.append((glyph_x, [char]))
                    prev_was_singlebyte = True
                else:
                    multibyte_glyphs.append((glyph_x, glyph_idx))
                    prev_was_singlebyte = False
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
            for start_x, chars in singlebyte_chunks:
                self._setup_textpos(start_x, 0, 0, prev_start_x, 0, 0)
                self.file.output(self.encode_string(''.join(chars), fonttype),
                                 Op.show)
                prev_start_x = start_x
            self.file.output(Op.end_text)
            # Then emit all the multibyte characters, one at a time.
            for start_x, glyph_idx in multibyte_glyphs:
                glyph_name = font.get_glyph_name(glyph_idx)
                self.file.output(Op.gsave)
                self.file.output(0.001 * fontsize, 0,
                                 0, 0.001 * fontsize,
                                 start_x, 0, Op.concat_matrix)
                name = self.file._get_xobject_symbol_name(
                    font.fname, glyph_name)
                self.file.output(Name(name), Op.use_xobject)
                self.file.output(Op.grestore)
            self.file.output(Op.grestore)
