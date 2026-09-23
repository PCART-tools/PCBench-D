    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        if debugPS:
            self._pswriter.write("% text\n")

        if _is_transparent(gc.get_rgb()):
            return  # Special handling for fully transparent.

        if ismath == 'TeX':
            return self.draw_tex(gc, x, y, s, prop, angle)

        elif ismath:
            return self.draw_mathtext(gc, x, y, s, prop, angle)

        elif mpl.rcParams['ps.useafm']:
            self.set_color(*gc.get_rgb())

            font = self._get_font_afm(prop)
            fontname = font.get_fontname()
            fontsize = prop.get_size_in_points()
            scale = 0.001 * fontsize

            thisx = 0
            thisy = font.get_str_bbox_and_descent(s)[4] * scale
            last_name = None
            lines = []
            for c in s:
                name = uni2type1.get(ord(c), f"uni{ord(c):04X}")
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

                lines.append('%f %f m /%s glyphshow' % (thisx, thisy, name))

                thisx += width * scale

            thetext = "\n".join(lines)
            self._pswriter.write(f"""\
gsave
/{fontname} findfont
{fontsize} scalefont
setfont
{x:f} {y:f} translate
{angle:f} rotate
{thetext}
grestore
""")

        else:
            font = self._get_font_ttf(prop)
            font.set_text(s, 0, flags=LOAD_NO_HINTING)
            self._character_tracker.track(font, s)

            self.set_color(*gc.get_rgb())
            ps_name = (font.postscript_name
                       .encode('ascii', 'replace').decode('ascii'))
            self.set_font(ps_name, prop.get_size_in_points())

            thetext = '\n'.join(
                '%f 0 m /%s glyphshow' % (x, font.get_glyph_name(glyph_idx))
                for glyph_idx, x in _text_layout.layout(s, font))
            self._pswriter.write(f"""\
gsave
{x:f} {y:f} translate
{angle:f} rotate
{thetext}
grestore
""")
