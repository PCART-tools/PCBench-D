    @_log_if_debug_on
    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        if self._is_transparent(gc.get_rgb()):
            return  # Special handling for fully transparent.

        if ismath == 'TeX':
            return self.draw_tex(gc, x, y, s, prop, angle)

        if ismath:
            return self.draw_mathtext(gc, x, y, s, prop, angle)

        if mpl.rcParams['ps.useafm']:
            font = self._get_font_afm(prop)
            scale = 0.001 * prop.get_size_in_points()

            thisx = 0
            last_name = None  # kerns returns 0 for None.
            xs_names = []
            for c in s:
                name = uni2type1.get(ord(c), f"uni{ord(c):04X}")
                try:
                    width = font.get_width_from_char_name(name)
                except KeyError:
                    name = 'question'
                    width = font.get_width_char('?')
                kern = font.get_kern_dist_from_name(last_name, name)
                last_name = name
                thisx += kern * scale
                xs_names.append((thisx, name))
                thisx += width * scale

        else:
            font = self._get_font_ttf(prop)
            font.set_text(s, 0, flags=LOAD_NO_HINTING)
            self._character_tracker.track(font, s)
            xs_names = [(item.x, font.get_glyph_name(item.glyph_idx))
                        for item in _text_helpers.layout(s, font)]

        self.set_color(*gc.get_rgb())
        ps_name = (font.postscript_name
                   .encode("ascii", "replace").decode("ascii"))
        self.set_font(ps_name, prop.get_size_in_points())
        thetext = "\n".join(f"{x:f} 0 m /{name:s} glyphshow"
                            for x, name in xs_names)
        self._pswriter.write(f"""\
gsave
{self._get_clip_cmd(gc)}
{x:f} {y:f} translate
{angle:f} rotate
{thetext}
grestore
""")
