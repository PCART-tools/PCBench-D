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
            stream = []
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
            ps_name = (font.postscript_name
                       .encode("ascii", "replace").decode("ascii"))
            stream.append((ps_name, xs_names))

        else:
            font = self._get_font_ttf(prop)
            self._character_tracker.track(font, s)
            stream = []
            prev_font = curr_stream = None
            for item in _text_helpers.layout(s, font):
                ps_name = (item.ft_object.postscript_name
                           .encode("ascii", "replace").decode("ascii"))
                if item.ft_object is not prev_font:
                    if curr_stream:
                        stream.append(curr_stream)
                    prev_font = item.ft_object
                    curr_stream = [ps_name, []]
                curr_stream[1].append(
                    (item.x, item.ft_object.get_glyph_name(item.glyph_idx))
                )
            # append the last entry
            stream.append(curr_stream)

        self.set_color(*gc.get_rgb())

        for ps_name, xs_names in stream:
            self.set_font(ps_name, prop.get_size_in_points(), False)
            thetext = "\n".join(f"{x:g} 0 m /{name:s} glyphshow"
                                for x, name in xs_names)
            self._pswriter.write(f"""\
gsave
{self._get_clip_cmd(gc)}
{x:g} {y:g} translate
{angle:g} rotate
{thetext}
grestore
""")
