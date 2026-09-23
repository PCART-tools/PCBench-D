    def _get_style_dict(self, gc, rgbFace):
        """Generate a style string from the GraphicsContext and rgbFace."""
        attrib = {}

        forced_alpha = gc.get_forced_alpha()

        if gc.get_hatch() is not None:
            attrib['fill'] = "url(#%s)" % self._get_hatch(gc, rgbFace)
            if (rgbFace is not None and len(rgbFace) == 4 and rgbFace[3] != 1.0
                    and not forced_alpha):
                attrib['fill-opacity'] = short_float_fmt(rgbFace[3])
        else:
            if rgbFace is None:
                attrib['fill'] = 'none'
            else:
                if tuple(rgbFace[:3]) != (0, 0, 0):
                    attrib['fill'] = rgb2hex(rgbFace)
                if (len(rgbFace) == 4 and rgbFace[3] != 1.0
                        and not forced_alpha):
                    attrib['fill-opacity'] = short_float_fmt(rgbFace[3])

        if forced_alpha and gc.get_alpha() != 1.0:
            attrib['opacity'] = short_float_fmt(gc.get_alpha())

        offset, seq = gc.get_dashes()
        if seq is not None:
            attrib['stroke-dasharray'] = ','.join(
                short_float_fmt(val) for val in seq)
            attrib['stroke-dashoffset'] = short_float_fmt(float(offset))

        linewidth = gc.get_linewidth()
        if linewidth:
            rgb = gc.get_rgb()
            attrib['stroke'] = rgb2hex(rgb)
            if not forced_alpha and rgb[3] != 1.0:
                attrib['stroke-opacity'] = short_float_fmt(rgb[3])
            if linewidth != 1.0:
                attrib['stroke-width'] = short_float_fmt(linewidth)
            if gc.get_joinstyle() != 'round':
                attrib['stroke-linejoin'] = gc.get_joinstyle()
            if gc.get_capstyle() != 'butt':
                attrib['stroke-linecap'] = _capstyle_d[gc.get_capstyle()]

        return attrib
