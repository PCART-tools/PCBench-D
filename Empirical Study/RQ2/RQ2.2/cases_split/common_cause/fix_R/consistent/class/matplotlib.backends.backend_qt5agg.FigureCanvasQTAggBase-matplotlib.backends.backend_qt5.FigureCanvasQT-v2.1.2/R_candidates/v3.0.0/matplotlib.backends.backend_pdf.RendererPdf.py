class RendererPdf(RendererBase):
    afm_font_cache = maxdict(50)

    def __init__(self, file, image_dpi, height, width):
        RendererBase.__init__(self)
        self.height = height
        self.width = width
        self.file = file
        self.gc = self.new_gc()
        self.mathtext_parser = MathTextParser("Pdf")
        self.image_dpi = image_dpi

    def finalize(self):
        self.file.output(*self.gc.finalize())

    def check_gc(self, gc, fillcolor=None):
        orig_fill = getattr(gc, '_fillcolor', (0., 0., 0.))
        gc._fillcolor = fillcolor

        orig_alphas = getattr(gc, '_effective_alphas', (1.0, 1.0))

        if gc.get_rgb() is None:
            # it should not matter what color here
            # since linewidth should be 0
            # unless affected by global settings in rcParams
            # hence setting zero alpha just incase
            gc.set_foreground((0, 0, 0, 0), isRGBA=True)

        if gc._forced_alpha:
            gc._effective_alphas = (gc._alpha, gc._alpha)
        elif fillcolor is None or len(fillcolor) < 4:
            gc._effective_alphas = (gc._rgb[3], 1.0)
        else:
            gc._effective_alphas = (gc._rgb[3], fillcolor[3])

        delta = self.gc.delta(gc)
        if delta:
            self.file.output(*delta)

        # Restore gc to avoid unwanted side effects
        gc._fillcolor = orig_fill
        gc._effective_alphas = orig_alphas

    def track_characters(self, font, s):
        """Keeps track of which characters are required from
        each font."""
        if isinstance(font, str):
            fname = font
        else:
            fname = font.fname
        realpath, stat_key = get_realpath_and_stat(fname)
        used_characters = self.file.used_characters.setdefault(
            stat_key, (realpath, set()))
        used_characters[1].update(map(ord, s))

    def merge_used_characters(self, other):
        for stat_key, (realpath, charset) in other.items():
            used_characters = self.file.used_characters.setdefault(
                stat_key, (realpath, set()))
            used_characters[1].update(charset)

    def get_image_magnification(self):
        return self.image_dpi/72.0

    def option_scale_image(self):
        """
        pdf backend support arbitrary scaling of image.
        """
        return True

    def option_image_nocomposite(self):
        """
        return whether to generate a composite image from multiple images on
        a set of axes
        """
        return not rcParams['image.composite_image']

    def draw_image(self, gc, x, y, im, transform=None):
        h, w = im.shape[:2]
        if w == 0 or h == 0:
            return

        if transform is None:
            # If there's no transform, alpha has already been applied
            gc.set_alpha(1.0)

        self.check_gc(gc)

        w = 72.0 * w / self.image_dpi
        h = 72.0 * h / self.image_dpi

        imob = self.file.imageObject(im)

        if transform is None:
            self.file.output(Op.gsave,
                             w, 0, 0, h, x, y, Op.concat_matrix,
                             imob, Op.use_xobject, Op.grestore)
        else:
            tr1, tr2, tr3, tr4, tr5, tr6 = transform.frozen().to_values()

            self.file.output(Op.gsave,
                             1, 0, 0, 1, x, y, Op.concat_matrix,
                             tr1, tr2, tr3, tr4, tr5, tr6, Op.concat_matrix,
                             imob, Op.use_xobject, Op.grestore)

    def draw_path(self, gc, path, transform, rgbFace=None):
        self.check_gc(gc, rgbFace)
        self.file.writePath(
            path, transform,
            rgbFace is None and gc.get_hatch_path() is None,
            gc.get_sketch_params())
        self.file.output(self.gc.paint())

    def draw_path_collection(self, gc, master_transform, paths, all_transforms,
                             offsets, offsetTrans, facecolors, edgecolors,
                             linewidths, linestyles, antialiaseds, urls,
                             offset_position):
        # We can only reuse the objects if the presence of fill and
        # stroke (and the amount of alpha for each) is the same for
        # all of them
        can_do_optimization = True
        facecolors = np.asarray(facecolors)
        edgecolors = np.asarray(edgecolors)

        if not len(facecolors):
            filled = False
            can_do_optimization = not gc.get_hatch()
        else:
            if np.all(facecolors[:, 3] == facecolors[0, 3]):
                filled = facecolors[0, 3] != 0.0
            else:
                can_do_optimization = False

        if not len(edgecolors):
            stroked = False
        else:
            if np.all(np.asarray(linewidths) == 0.0):
                stroked = False
            elif np.all(edgecolors[:, 3] == edgecolors[0, 3]):
                stroked = edgecolors[0, 3] != 0.0
            else:
                can_do_optimization = False

        # Is the optimization worth it? Rough calculation:
        # cost of emitting a path in-line is len_path * uses_per_path
        # cost of XObject is len_path + 5 for the definition,
        #    uses_per_path for the uses
        len_path = len(paths[0].vertices) if len(paths) > 0 else 0
        uses_per_path = self._iter_collection_uses_per_path(
            paths, all_transforms, offsets, facecolors, edgecolors)
        should_do_optimization = \
            len_path + uses_per_path + 5 < len_path * uses_per_path

        if (not can_do_optimization) or (not should_do_optimization):
            return RendererBase.draw_path_collection(
                self, gc, master_transform, paths, all_transforms,
                offsets, offsetTrans, facecolors, edgecolors,
                linewidths, linestyles, antialiaseds, urls,
                offset_position)

        padding = np.max(linewidths)
        path_codes = []
        for i, (path, transform) in enumerate(self._iter_collection_raw_paths(
                master_transform, paths, all_transforms)):
            name = self.file.pathCollectionObject(
                gc, path, transform, padding, filled, stroked)
            path_codes.append(name)

        output = self.file.output
        output(*self.gc.push())
        lastx, lasty = 0, 0
        for xo, yo, path_id, gc0, rgbFace in self._iter_collection(
                gc, master_transform, all_transforms, path_codes, offsets,
                offsetTrans, facecolors, edgecolors, linewidths, linestyles,
                antialiaseds, urls, offset_position):

            self.check_gc(gc0, rgbFace)
            dx, dy = xo - lastx, yo - lasty
            output(1, 0, 0, 1, dx, dy, Op.concat_matrix, path_id,
                   Op.use_xobject)
            lastx, lasty = xo, yo
        output(*self.gc.pop())

    def draw_markers(self, gc, marker_path, marker_trans, path, trans,
                     rgbFace=None):
        # Same logic as in draw_path_collection
        len_marker_path = len(marker_path)
        uses = len(path)
        if len_marker_path * uses < len_marker_path + uses + 5:
            RendererBase.draw_markers(self, gc, marker_path, marker_trans,
                                      path, trans, rgbFace)
            return

        self.check_gc(gc, rgbFace)
        fill = gc.fill(rgbFace)
        stroke = gc.stroke()

        output = self.file.output
        marker = self.file.markerObject(
            marker_path, marker_trans, fill, stroke, self.gc._linewidth,
            gc.get_joinstyle(), gc.get_capstyle())

        output(Op.gsave)
        lastx, lasty = 0, 0
        for vertices, code in path.iter_segments(
                trans,
                clip=(0, 0, self.file.width*72, self.file.height*72),
                simplify=False):
            if len(vertices):
                x, y = vertices[-2:]
                if not (0 <= x <= self.file.width * 72
                        and 0 <= y <= self.file.height * 72):
                    continue
                dx, dy = x - lastx, y - lasty
                output(1, 0, 0, 1, dx, dy, Op.concat_matrix,
                       marker, Op.use_xobject)
                lastx, lasty = x, y
        output(Op.grestore)

    def draw_gouraud_triangle(self, gc, points, colors, trans):
        self.draw_gouraud_triangles(gc, points.reshape((1, 3, 2)),
                                    colors.reshape((1, 3, 4)), trans)

    def draw_gouraud_triangles(self, gc, points, colors, trans):
        assert len(points) == len(colors)
        assert points.ndim == 3
        assert points.shape[1] == 3
        assert points.shape[2] == 2
        assert colors.ndim == 3
        assert colors.shape[1] == 3
        assert colors.shape[2] == 4

        shape = points.shape
        points = points.reshape((shape[0] * shape[1], 2))
        tpoints = trans.transform(points)
        tpoints = tpoints.reshape(shape)
        name = self.file.addGouraudTriangles(tpoints, colors)
        self.check_gc(gc)
        self.file.output(name, Op.shading)

    def _setup_textpos(self, x, y, angle, oldx=0, oldy=0, oldangle=0):
        if angle == oldangle == 0:
            self.file.output(x - oldx, y - oldy, Op.textpos)
        else:
            angle = angle / 180.0 * pi
            self.file.output(cos(angle), sin(angle),
                             -sin(angle), cos(angle),
                             x, y, Op.textmatrix)
            self.file.output(0, 0, Op.textpos)

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

    def draw_tex(self, gc, x, y, s, prop, angle, ismath='TeX!', mtext=None):
        texmanager = self.get_texmanager()
        fontsize = prop.get_size_in_points()
        dvifile = texmanager.make_dvi(s, fontsize)
        with dviread.Dvi(dvifile, 72) as dvi:
            page = next(iter(dvi))

        # Gather font information and do some setup for combining
        # characters into strings. The variable seq will contain a
        # sequence of font and text entries. A font entry is a list
        # ['font', name, size] where name is a Name object for the
        # font. A text entry is ['text', x, y, glyphs, x+w] where x
        # and y are the starting coordinates, w is the width, and
        # glyphs is a list; in this phase it will always contain just
        # one one-character string, but later it may have longer
        # strings interspersed with kern amounts.
        oldfont, seq = None, []
        for x1, y1, dvifont, glyph, width in page.text:
            if dvifont != oldfont:
                pdfname = self.file.dviFontName(dvifont)
                seq += [['font', pdfname, dvifont.size]]
                oldfont = dvifont
            seq += [['text', x1, y1, [bytes([glyph])], x1+width]]

        # Find consecutive text strings with constant y coordinate and
        # combine into a sequence of strings and kerns, or just one
        # string (if any kerns would be less than 0.1 points).
        i, curx, fontsize = 0, 0, None
        while i < len(seq)-1:
            elt, nxt = seq[i:i+2]
            if elt[0] == 'font':
                fontsize = elt[2]
            elif elt[0] == nxt[0] == 'text' and elt[2] == nxt[2]:
                offset = elt[4] - nxt[1]
                if abs(offset) < 0.1:
                    elt[3][-1] += nxt[3][0]
                    elt[4] += nxt[4]-nxt[1]
                else:
                    elt[3] += [offset*1000.0/fontsize, nxt[3][0]]
                    elt[4] = nxt[4]
                del seq[i+1]
                continue
            i += 1

        # Create a transform to map the dvi contents to the canvas.
        mytrans = Affine2D().rotate_deg(angle).translate(x, y)

        # Output the text.
        self.check_gc(gc, gc._rgb)
        self.file.output(Op.begin_text)
        curx, cury, oldx, oldy = 0, 0, 0, 0
        for elt in seq:
            if elt[0] == 'font':
                self.file.output(elt[1], elt[2], Op.selectfont)
            elif elt[0] == 'text':
                curx, cury = mytrans.transform_point((elt[1], elt[2]))
                self._setup_textpos(curx, cury, angle, oldx, oldy)
                oldx, oldy = curx, cury
                if len(elt[3]) == 1:
                    self.file.output(elt[3][0], Op.show)
                else:
                    self.file.output(elt[3], Op.showkern)
            else:
                assert False
        self.file.output(Op.end_text)

        # Then output the boxes (e.g., variable-length lines of square
        # roots).
        boxgc = self.new_gc()
        boxgc.copy_properties(gc)
        boxgc.set_linewidth(0)
        pathops = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                   Path.CLOSEPOLY]
        for x1, y1, h, w in page.boxes:
            path = Path([[x1, y1], [x1+w, y1], [x1+w, y1+h], [x1, y1+h],
                         [0, 0]], pathops)
            self.draw_path(boxgc, path, mytrans, gc._rgb)

    def encode_string(self, s, fonttype):
        if fonttype in (1, 3):
            return s.encode('cp1252', 'replace')
        return s.encode('utf-16be', 'replace')

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
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
            l, b, w, h = font.get_str_bbox(s)
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
            """Determine if we should use the simple or woven method
            to output this text, and chunks the string into 1-byte and
            2-byte sections if necessary."""
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
            """Outputs text using the woven method, alternating
            between chunks of 1-byte characters and 2-byte characters.
            Only used for Type 3 fonts."""
            chunks = [(a, ''.join(b)) for a, b in chunks]

            # Do the rotation and global translation as a single matrix
            # concatenation up front
            self.file.output(Op.gsave)
            a = angle / 180.0 * pi
            self.file.output(cos(a), sin(a), -sin(a), cos(a), x, y,
                             Op.concat_matrix)

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

    def get_text_width_height_descent(self, s, prop, ismath):
        if rcParams['text.usetex']:
            texmanager = self.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(s, fontsize,
                                                               renderer=self)
            return w, h, d

        if ismath:
            w, h, d, glyphs, rects, used_characters = \
                self.mathtext_parser.parse(s, 72, prop)

        elif rcParams['pdf.use14corefonts']:
            font = self._get_font_afm(prop)
            l, b, w, h, d = font.get_str_bbox_and_descent(s)
            scale = prop.get_size_in_points()
            w *= scale / 1000
            h *= scale / 1000
            d *= scale / 1000
        else:
            font = self._get_font_ttf(prop)
            font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
            w, h = font.get_width_height()
            scale = (1.0 / 64.0)
            w *= scale
            h *= scale
            d = font.get_descent()
            d *= scale
        return w, h, d

    def _get_font_afm(self, prop):
        key = hash(prop)
        font = self.afm_font_cache.get(key)
        if font is None:
            filename = findfont(
                prop, fontext='afm', directory=self.file._core14fontdir)
            if filename is None:
                filename = findfont(
                    "Helvetica", fontext='afm',
                    directory=self.file._core14fontdir)
            font = self.afm_font_cache.get(filename)
            if font is None:
                with open(filename, 'rb') as fh:
                    font = AFM(fh)
                    self.afm_font_cache[filename] = font
            self.afm_font_cache[key] = font
        return font

    def _get_font_ttf(self, prop):
        filename = findfont(prop)
        font = get_font(filename)
        font.clear()
        font.set_size(prop.get_size_in_points(), 72)
        return font

    def flipy(self):
        return False

    def get_canvas_width_height(self):
        return self.file.width * 72.0, self.file.height * 72.0

    def new_gc(self):
        return GraphicsContextPdf(self.file)
