    @_log_if_debug_on
    def draw_tex(self, gc, x, y, s, prop, angle, *, mtext=None):
        # docstring inherited
        if self._is_transparent(gc.get_rgb()):
            return  # Special handling for fully transparent.

        if not hasattr(self, "psfrag"):
            self._logwarn_once(
                "The PS backend determines usetex status solely based on "
                "rcParams['text.usetex'] and does not support having "
                "usetex=True only for some elements; this element will thus "
                "be rendered as if usetex=False.")
            self.draw_text(gc, x, y, s, prop, angle, False, mtext)
            return

        w, h, bl = self.get_text_width_height_descent(s, prop, ismath="TeX")
        fontsize = prop.get_size_in_points()
        thetext = 'psmarker%d' % self.textcnt
        color = '%1.3f,%1.3f,%1.3f' % gc.get_rgb()[:3]
        fontcmd = {'sans-serif': r'{\sffamily %s}',
                   'monospace': r'{\ttfamily %s}'}.get(
                       mpl.rcParams['font.family'][0], r'{\rmfamily %s}')
        s = fontcmd % s
        tex = r'\color[rgb]{%s} %s' % (color, s)

        # Stick to the bottom alignment.
        pos = _nums_to_str(x, y-bl)
        self.psfrag.append(
            r'\psfrag{%s}[bl][bl][1][%f]{\fontsize{%f}{%f}%s}' % (
                thetext, angle, fontsize, fontsize*1.25, tex))

        self._pswriter.write(f"""\
gsave
{pos} moveto
({thetext})
show
grestore
""")
        self.textcnt += 1
