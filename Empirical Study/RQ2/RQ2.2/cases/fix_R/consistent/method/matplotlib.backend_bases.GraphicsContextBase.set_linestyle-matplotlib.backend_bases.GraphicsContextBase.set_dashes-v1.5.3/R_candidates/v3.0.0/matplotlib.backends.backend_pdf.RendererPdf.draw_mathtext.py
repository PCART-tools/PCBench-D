    def draw_mathtext(self, gc, x, y, s, prop, angle):
        # TODO: fix positioning and encoding
        width, height, descent, glyphs, rects, used_characters = \
            self.mathtext_parser.parse(s, 72, prop)
        self.merge_used_characters(used_characters)

        # When using Type 3 fonts, we can't use character codes higher
        # than 255, so we use the "Do" command to render those
        # instead.
        global_fonttype = rcParams['pdf.fonttype']

        # Set up a global transformation matrix for the whole math expression
        a = angle / 180.0 * pi
        self.file.output(Op.gsave)
        self.file.output(cos(a), sin(a), -sin(a), cos(a), x, y,
                         Op.concat_matrix)

        self.check_gc(gc, gc._rgb)
        self.file.output(Op.begin_text)
        prev_font = None, None
        oldx, oldy = 0, 0
        for ox, oy, fontname, fontsize, num, symbol_name in glyphs:
            if is_opentype_cff_font(fontname):
                fonttype = 42
            else:
                fonttype = global_fonttype

            if fonttype == 42 or num <= 255:
                self._setup_textpos(ox, oy, 0, oldx, oldy)
                oldx, oldy = ox, oy
                if (fontname, fontsize) != prev_font:
                    self.file.output(self.file.fontName(fontname), fontsize,
                                     Op.selectfont)
                    prev_font = fontname, fontsize
                self.file.output(self.encode_string(chr(num), fonttype),
                                 Op.show)
        self.file.output(Op.end_text)

        # If using Type 3 fonts, render all of the multi-byte characters
        # as XObjects using the 'Do' command.
        if global_fonttype == 3:
            for ox, oy, fontname, fontsize, num, symbol_name in glyphs:
                if is_opentype_cff_font(fontname):
                    fonttype = 42
                else:
                    fonttype = global_fonttype

                if fonttype == 3 and num > 255:
                    self.file.fontName(fontname)
                    self.file.output(Op.gsave,
                                     0.001 * fontsize, 0,
                                     0, 0.001 * fontsize,
                                     ox, oy, Op.concat_matrix)
                    name = self.file._get_xobject_symbol_name(
                        fontname, symbol_name)
                    self.file.output(Name(name), Op.use_xobject)
                    self.file.output(Op.grestore)

        # Draw any horizontal lines in the math layout
        for ox, oy, width, height in rects:
            self.file.output(Op.gsave, ox, oy, width, height,
                             Op.rectangle, Op.fill, Op.grestore)

        # Pop off the global transformation
        self.file.output(Op.grestore)
