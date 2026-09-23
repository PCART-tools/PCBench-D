    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        # TODO: combine consecutive texts into one BT/ET delimited section

        # This function is rather complex, since there is no way to
        # access characters of a Type 3 font with codes > 255.  (Type
        # 3 fonts can not have a CIDMap).  Therefore, we break the
        # string into chunks, where each chunk contains exclusively
        # 1-byte or exclusively 2-byte characters, and output each
        # chunk a separate command.  1-byte characters use the regular
        # text show command (Tj), whereas 2-byte characters use the
        # use XObject command (Do).  If using Type 42 fonts, all of
        # this complication is avoided, but of course, those fonts can
        # not be subsetted.

        self.check_gc(gc, gc._rgb)
        if ismath:
            return self.draw_mathtext(gc, x, y, s, prop, angle)

        fontsize = prop.get_size_in_points()

        if rcParams['pdf.use14corefonts']:
            font = self._get_font_afm(prop)
            fonttype = 1
        else:
            font = self._get_font_ttf(prop)
            self.track_characters(font, s)
            font.set_text(s, 0.0, flags=LOAD_NO_HINTING)

            fonttype = rcParams['pdf.fonttype']

            # We can't subset all OpenType fonts, so switch to Type 42
            # in that case.
            if is_opentype_cff_font(font.fname):
                fonttype = 42

        def check_simple_method(s):
            """
            Determine if we should use the simple or woven method to output
            this text, and chunks the string into 1-byte and 2-byte sections if
            necessary.
            """
            use_simple_method = True
            chunks = []

            if not rcParams['pdf.use14corefonts']:
                if fonttype == 3 and not isinstance(s, bytes) and len(s) != 0:
                    # Break the string into chunks where each chunk is either
                    # a string of chars <= 255, or a single character > 255.
                    s = str(s)
                    for c in s:
                        if ord(c) <= 255:
                            char_type = 1
                        else:
                            char_type = 2
                        if len(chunks) and chunks[-1][0] == char_type:
                            chunks[-1][1].append(c)
                        else:
                            chunks.append((char_type, [c]))
                    use_simple_method = (len(chunks) == 1 and
                                         chunks[-1][0] == 1)
            return use_simple_method, chunks

        def draw_text_simple():
            """Outputs text using the simple method."""
            self.file.output(Op.begin_text,
                             self.file.fontName(prop),
                             fontsize,
                             Op.selectfont)
            self._setup_textpos(x, y, angle)
            self.file.output(self.encode_string(s, fonttype), Op.show,
                             Op.end_text)

        def draw_text_woven(chunks):
            """
            Outputs text using the woven method, alternating between chunks of
            1-byte and 2-byte characters.  Only used for Type 3 fonts.
            """
            chunks = [(a, ''.join(b)) for a, b in chunks]

            # Do the rotation and global translation as a single matrix
            # concatenation up front
            self.file.output(Op.gsave)
            a = math.radians(angle)
            self.file.output(math.cos(a), math.sin(a),
                             -math.sin(a), math.cos(a),
                             x, y, Op.concat_matrix)

            # Output all the 1-byte characters in a BT/ET group, then
            # output all the 2-byte characters.
            for mode in (1, 2):
                newx = oldx = 0
                # Output a 1-byte character chunk
                if mode == 1:
                    self.file.output(Op.begin_text,
                                     self.file.fontName(prop),
                                     fontsize,
                                     Op.selectfont)

                for chunk_type, chunk in chunks:
                    if mode == 1 and chunk_type == 1:
                        self._setup_textpos(newx, 0, 0, oldx, 0, 0)
                        self.file.output(self.encode_string(chunk, fonttype),
                                         Op.show)
                        oldx = newx

                    lastgind = None
                    for c in chunk:
                        ccode = ord(c)
                        gind = font.get_char_index(ccode)
                        if gind is not None:
                            if mode == 2 and chunk_type == 2:
                                glyph_name = font.get_glyph_name(gind)
                                self.file.output(Op.gsave)
                                self.file.output(0.001 * fontsize, 0,
                                                 0, 0.001 * fontsize,
                                                 newx, 0, Op.concat_matrix)
                                name = self.file._get_xobject_symbol_name(
                                    font.fname, glyph_name)
                                self.file.output(Name(name), Op.use_xobject)
                                self.file.output(Op.grestore)

                            # Move the pointer based on the character width
                            # and kerning
                            glyph = font.load_char(ccode,
                                                   flags=LOAD_NO_HINTING)
                            if lastgind is not None:
                                kern = font.get_kerning(
                                    lastgind, gind, KERNING_UNFITTED)
                            else:
                                kern = 0
                            lastgind = gind
                            newx += kern/64.0 + glyph.linearHoriAdvance/65536.0

                if mode == 1:
                    self.file.output(Op.end_text)

            self.file.output(Op.grestore)

        use_simple_method, chunks = check_simple_method(s)
        if use_simple_method:
            return draw_text_simple()
        else:
            return draw_text_woven(chunks)
