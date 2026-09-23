    def draw_tex(self, gc, x, y, s, prop, angle, *, mtext=None):
        # docstring inherited
        texmanager = self.get_texmanager()
        fontsize = prop.get_size_in_points()
        dvifile = texmanager.make_dvi(s, fontsize)
        with dviread.Dvi(dvifile, 72) as dvi:
            page, = dvi

        if gc.get_url() is not None:
            self.file._annotations[-1][1].append(_get_link_annotation(
                gc, x, y, page.width, page.height, angle))

        # Gather font information and do some setup for combining
        # characters into strings. The variable seq will contain a
        # sequence of font and text entries. A font entry is a list
        # ['font', name, size] where name is a Name object for the
        # font. A text entry is ['text', x, y, glyphs, x+w] where x
        # and y are the starting coordinates, w is the width, and
        # glyphs is a list; in this phase it will always contain just
        # one single-character string, but later it may have longer
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
                curx, cury = mytrans.transform((elt[1], elt[2]))
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
