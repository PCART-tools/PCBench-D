    def draw_tex(self, gc, x, y, s, prop, angle, ismath='TeX!', mtext=None):
        # docstring inherited

        w, h, bl = self.get_text_width_height_descent(s, prop, ismath)
        fontsize = prop.get_size_in_points()
        thetext = 'psmarker%d' % self.textcnt
        color = '%1.3f,%1.3f,%1.3f' % gc.get_rgb()[:3]
        fontcmd = {'sans-serif': r'{\sffamily %s}',
                   'monospace': r'{\ttfamily %s}'}.get(
                       rcParams['font.family'][0], r'{\rmfamily %s}')
        s = fontcmd % s
        tex = r'\color[rgb]{%s} %s' % (color, s)

        corr = 0  # w/2*(fontsize-10)/10
        if rcParams['text.latex.preview']:
            # use baseline alignment!
            pos = _nums_to_str(x-corr, y)
            self.psfrag.append(
                r'\psfrag{%s}[Bl][Bl][1][%f]{\fontsize{%f}{%f}%s}' % (
                    thetext, angle, fontsize, fontsize*1.25, tex))
        else:
            # Stick to the bottom alignment, but this may give incorrect
            # baseline some times.
            pos = _nums_to_str(x-corr, y-bl)
            self.psfrag.append(
                r'\psfrag{%s}[bl][bl][1][%f]{\fontsize{%f}{%f}%s}' % (
                    thetext, angle, fontsize, fontsize*1.25, tex))

        ps = """\
gsave
%(pos)s moveto
(%(thetext)s)
show
grestore
    """ % locals()

        self._pswriter.write(ps)
        self.textcnt += 1
