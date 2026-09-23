    def _draw_text_as_text(self, gc, x, y, s, prop, angle, ismath, mtext=None):
        writer = self.writer

        color = rgb2hex(gc.get_rgb())
        style = {}
        if color != '#000000':
            style['fill'] = color

        alpha = gc.get_alpha() if gc.get_forced_alpha() else gc.get_rgb()[3]
        if alpha != 1:
            style['opacity'] = short_float_fmt(alpha)

        if not ismath:
            font = self._get_font(prop)
            font.set_text(s, 0.0, flags=LOAD_NO_HINTING)

            attrib = {}
            # Must add "px" to workaround a Firefox bug
            style['font-size'] = short_float_fmt(prop.get_size()) + 'px'
            style['font-family'] = str(font.family_name)
            style['font-style'] = prop.get_style().lower()
            style['font-weight'] = str(prop.get_weight()).lower()
            attrib['style'] = generate_css(style)

            if mtext and (angle == 0 or mtext.get_rotation_mode() == "anchor"):
                # If text anchoring can be supported, get the original
                # coordinates and add alignment information.

                # Get anchor coordinates.
                transform = mtext.get_transform()
                ax, ay = transform.transform(mtext.get_unitless_position())
                ay = self.height - ay

                # Don't do vertical anchor alignment. Most applications do not
                # support 'alignment-baseline' yet. Apply the vertical layout
                # to the anchor point manually for now.
                angle_rad = np.deg2rad(angle)
                dir_vert = np.array([np.sin(angle_rad), np.cos(angle_rad)])
                v_offset = np.dot(dir_vert, [(x - ax), (y - ay)])
                ax = ax + v_offset * dir_vert[0]
                ay = ay + v_offset * dir_vert[1]

                ha_mpl_to_svg = {'left': 'start', 'right': 'end',
                                 'center': 'middle'}
                style['text-anchor'] = ha_mpl_to_svg[mtext.get_ha()]

                attrib['x'] = short_float_fmt(ax)
                attrib['y'] = short_float_fmt(ay)
                attrib['style'] = generate_css(style)
                attrib['transform'] = "rotate(%s, %s, %s)" % (
                    short_float_fmt(-angle),
                    short_float_fmt(ax),
                    short_float_fmt(ay))
                writer.element('text', s, attrib=attrib)
            else:
                attrib['transform'] = generate_transform([
                    ('translate', (x, y)),
                    ('rotate', (-angle,))])

                writer.element('text', s, attrib=attrib)

        else:
            writer.comment(s)

            width, height, descent, svg_elements, used_characters = \
                self.mathtext_parser.parse(s, 72, prop)
            svg_glyphs = svg_elements.svg_glyphs
            svg_rects = svg_elements.svg_rects

            attrib = {}
            attrib['style'] = generate_css(style)
            attrib['transform'] = generate_transform([
                ('translate', (x, y)),
                ('rotate', (-angle,))])

            # Apply attributes to 'g', not 'text', because we likely have some
            # rectangles as well with the same style and transformation.
            writer.start('g', attrib=attrib)

            writer.start('text')

            # Sort the characters by font, and output one tspan for each.
            spans = OrderedDict()
            for font, fontsize, thetext, new_x, new_y, metrics in svg_glyphs:
                style = generate_css({
                    'font-size': short_float_fmt(fontsize) + 'px',
                    'font-family': font.family_name,
                    'font-style': font.style_name.lower(),
                    'font-weight': font.style_name.lower()})
                if thetext == 32:
                    thetext = 0xa0  # non-breaking space
                spans.setdefault(style, []).append((new_x, -new_y, thetext))

            for style, chars in spans.items():
                chars.sort()

                if len({y for x, y, t in chars}) == 1:  # Are all y's the same?
                    ys = str(chars[0][1])
                else:
                    ys = ' '.join(str(c[1]) for c in chars)

                attrib = {
                    'style': style,
                    'x': ' '.join(short_float_fmt(c[0]) for c in chars),
                    'y': ys
                    }

                writer.element(
                    'tspan',
                    ''.join(chr(c[2]) for c in chars),
                    attrib=attrib)

            writer.end('text')

            if len(svg_rects):
                for x, y, width, height in svg_rects:
                    writer.element(
                        'rect',
                        x=short_float_fmt(x),
                        y=short_float_fmt(-y + height),
                        width=short_float_fmt(width),
                        height=short_float_fmt(height)
                        )

            writer.end('g')
