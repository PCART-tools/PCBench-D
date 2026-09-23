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
            self.file._annotations[-1][1].append(_get_link_annotation(
                gc, x, y, width / 64, height / 64, angle))

        # If fonttype is neither 3 nor 42, emit the whole string at once
        # without manual kerning.
        if fonttype not in [3, 42]:
            self.file.output(Op.begin_text,
                             self.file.fontName(prop), fontsize, Op.selectfont)
            self._setup_textpos(x, y, angle)
            self.file.output(self.encode_string(s, fonttype),
                             Op.show, Op.end_text)

        # A sequence of characters is broken into multiple chunks. The chunking
        # serves two purposes:
        #   - For Type 3 fonts, there is no way to access multibyte characters,
        #     as they cannot have a CIDMap.  Therefore, in this case we break
        #     the string into chunks, where each chunk contains either a string
        #     of consecutive 1-byte characters or a single multibyte character.
        #   - A sequence of 1-byte characters is split into chunks to allow for
        #     kerning adjustments between consecutive chunks.
        #
        # Each chunk is emitted with a separate command: 1-byte characters use
        # the regular text show command (TJ) with appropriate kerning between
        # chunks, whereas multibyte characters use the XObject command (Do).
        else:
            # List of (ft_object, start_x, [prev_kern, char, char, ...]),
            # w/o zero kerns.
            singlebyte_chunks = []
            # List of (ft_object, start_x, glyph_index).
            multibyte_glyphs = []
            prev_was_multibyte = True
            prev_font = font
            for item in _text_helpers.layout(
                    s, font, kern_mode=KERNING_UNFITTED):
                if _font_supports_glyph(fonttype, ord(item.char)):
                    if prev_was_multibyte or item.ft_object != prev_font:
                        singlebyte_chunks.append((item.ft_object, item.x, []))
                        prev_font = item.ft_object
                    if item.prev_kern:
                        singlebyte_chunks[-1][2].append(item.prev_kern)
                    singlebyte_chunks[-1][2].append(item.char)
                    prev_was_multibyte = False
                else:
                    multibyte_glyphs.append(
                        (item.ft_object, item.x, item.glyph_idx)
                    )
                    prev_was_multibyte = True
            # Do the rotation and global translation as a single matrix
            # concatenation up front
            self.file.output(Op.gsave)
            a = math.radians(angle)
            self.file.output(math.cos(a), math.sin(a),
                             -math.sin(a), math.cos(a),
                             x, y, Op.concat_matrix)
            # Emit all the 1-byte characters in a BT/ET group.

            self.file.output(Op.begin_text)
            prev_start_x = 0
            for ft_object, start_x, kerns_or_chars in singlebyte_chunks:
                ft_name = self.file.fontName(ft_object.fname)
                self.file.output(ft_name, fontsize, Op.selectfont)
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
            for ft_object, start_x, glyph_idx in multibyte_glyphs:
                self._draw_xobject_glyph(
                    ft_object, fontsize, glyph_idx, start_x, 0
                )
            self.file.output(Op.grestore)
