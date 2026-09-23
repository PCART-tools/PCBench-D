    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        """
        Draw a Text instance.
        """
        # local to avoid repeated attribute lookups
        write = self._pswriter.write
        if debugPS:
            write("% text\n")

        if len(gc.get_rgb()) == 4 and gc.get_rgb()[3] == 0:
            return  # Special handling for fully transparent.

        if ismath=='TeX':
            return self.draw_tex(gc, x, y, s, prop, angle)

        elif ismath:
            return self.draw_mathtext(gc, x, y, s, prop, angle)

        elif rcParams['ps.useafm']:
            self.set_color(*gc.get_rgb())

            font = self._get_font_afm(prop)
            fontname = font.get_fontname()
            fontsize = prop.get_size_in_points()
            scale = 0.001*fontsize

            thisx = 0
            thisy = font.get_str_bbox_and_descent(s)[4] * scale
            last_name = None
            lines = []
            for c in s:
                name = uni2type1.get(ord(c), 'question')
                try:
                    width = font.get_width_from_char_name(name)
                except KeyError:
                    name = 'question'
                    width = font.get_width_char('?')
                if last_name is not None:
                    kern = font.get_kern_dist_from_name(last_name, name)
                else:
                    kern = 0
                last_name = name
                thisx += kern * scale

                lines.append('%f %f m /%s glyphshow'%(thisx, thisy, name))

                thisx += width * scale

            thetext = "\n".join(lines)
            ps = """\
gsave
/%(fontname)s findfont
%(fontsize)s scalefont
setfont
%(x)f %(y)f translate
%(angle)f rotate
%(thetext)s
grestore
    """ % locals()
            self._pswriter.write(ps)

        else:
            font = self._get_font_ttf(prop)
            font.set_text(s, 0, flags=LOAD_NO_HINTING)
            self.track_characters(font, s)

            self.set_color(*gc.get_rgb())
            ps_name = (font.postscript_name
                       .encode('ascii', 'replace').decode('ascii'))
            self.set_font(ps_name, prop.get_size_in_points())

            lastgind = None
            lines = []
            thisx = 0
            thisy = 0
            for c in s:
                ccode = ord(c)
                gind = font.get_char_index(ccode)
                if gind is None:
                    ccode = ord('?')
                    name = '.notdef'
                    gind = 0
                else:
                    name = font.get_glyph_name(gind)
                glyph = font.load_char(ccode, flags=LOAD_NO_HINTING)

                if lastgind is not None:
                    kern = font.get_kerning(lastgind, gind, KERNING_DEFAULT)
                else:
                    kern = 0
                lastgind = gind
                thisx += kern/64.0

                lines.append('%f %f m /%s glyphshow'%(thisx, thisy, name))
                thisx += glyph.linearHoriAdvance/65536.0


            thetext = '\n'.join(lines)
            ps = """gsave
%(x)f %(y)f translate
%(angle)f rotate
%(thetext)s
grestore
""" % locals()
            self._pswriter.write(ps)
