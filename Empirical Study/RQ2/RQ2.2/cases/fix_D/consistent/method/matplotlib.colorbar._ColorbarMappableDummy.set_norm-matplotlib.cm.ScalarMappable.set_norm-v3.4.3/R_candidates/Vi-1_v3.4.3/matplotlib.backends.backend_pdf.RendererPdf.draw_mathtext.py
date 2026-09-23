    def draw_mathtext(self, gc, x, y, s, prop, angle):
        # TODO: fix positioning and encoding
        width, height, descent, glyphs, rects = \
            self._text2path.mathtext_parser.parse(s, 72, prop)

        if gc.get_url() is not None:
            link_annotation = {
                'Type': Name('Annot'),
                'Subtype': Name('Link'),
                'Rect': (x, y, x + width, y + height),
                'Border': [0, 0, 0],
                'A': {
                    'S': Name('URI'),
                    'URI': gc.get_url(),
                },
            }
            self.file._annotations[-1][1].append(link_annotation)

        fonttype = mpl.rcParams['pdf.fonttype']

        # Set up a global transformation matrix for the whole math expression
        a = math.radians(angle)
        self.file.output(Op.gsave)
        self.file.output(math.cos(a), math.sin(a),
                         -math.sin(a), math.cos(a),
                         x, y, Op.concat_matrix)

        self.check_gc(gc, gc._rgb)
        prev_font = None, None
        oldx, oldy = 0, 0
        type3_multibytes = []

        self.file.output(Op.begin_text)
        for font, fontsize, num, ox, oy in glyphs:
            self.file._character_tracker.track(font, chr(num))
            fontname = font.fname
            if fonttype == 3 and num > 255:
                # For Type3 fonts, multibyte characters must be emitted
                # separately (below).
                type3_multibytes.append((font, fontsize, ox, oy, num))
            else:
                self._setup_textpos(ox, oy, 0, oldx, oldy)
                oldx, oldy = ox, oy
                if (fontname, fontsize) != prev_font:
                    self.file.output(self.file.fontName(fontname), fontsize,
                                     Op.selectfont)
                    prev_font = fontname, fontsize
                self.file.output(self.encode_string(chr(num), fonttype),
                                 Op.show)
        self.file.output(Op.end_text)

        for font, fontsize, ox, oy, num in type3_multibytes:
            self._draw_xobject_glyph(
                font, fontsize, font.get_char_index(num), ox, oy)

        # Draw any horizontal lines in the math layout
        for ox, oy, width, height in rects:
            self.file.output(Op.gsave, ox, oy, width, height,
                             Op.rectangle, Op.fill, Op.grestore)

        # Pop off the global transformation
        self.file.output(Op.grestore)
