    def _draw_text_as_text(self, gc, x, y, s, prop, angle, ismath, mtext=None):
        # NOTE: If you change the font styling CSS, then be sure the check for
        # svg.fonttype = none in `lib/matplotlib/testing/compare.py::convert` remains in
        # sync. Also be sure to re-generate any SVG using this mode, or else such tests
        # will fail to use the right converter for the expected images, and they will
        # fail strangely.
        writer = self.writer

        color = rgb2hex(gc.get_rgb())
        font_style = {}
        color_style = {}
        if color != '#000000':
            color_style['fill'] = color

        alpha = gc.get_alpha() if gc.get_forced_alpha() else gc.get_rgb()[3]
        if alpha != 1:
            color_style['opacity'] = _short_float_fmt(alpha)

        if not ismath:
            attrib = {}

            # Separate font style in their separate attributes
            if prop.get_style() != 'normal':
                font_style['font-style'] = prop.get_style()
            if prop.get_variant() != 'normal':
                font_style['font-variant'] = prop.get_variant()
            weight = fm.weight_dict[prop.get_weight()]
            if weight != 400:
                font_style['font-weight'] = f'{weight}'

            def _normalize_sans(name):
                return 'sans-serif' if name in ['sans', 'sans serif'] else name

            def _expand_family_entry(fn):
                fn = _normalize_sans(fn)
                # prepend generic font families with all configured font names
                if fn in fm.font_family_aliases:
                    # get all of the font names and fix spelling of sans-serif
                    # (we accept 3 ways CSS only supports 1)
                    for name in fm.FontManager._expand_aliases(fn):
                        yield _normalize_sans(name)
                # whether a generic name or a family name, it must appear at
                # least once
                yield fn

            def _get_all_quoted_names(prop):
                # only quote specific names, not generic names
                return [name if name in fm.font_family_aliases else repr(name)
                        for entry in prop.get_family()
                        for name in _expand_family_entry(entry)]

            font_style['font-size'] = f'{_short_float_fmt(prop.get_size())}px'
            # ensure expansion, quoting, and dedupe of font names
            font_style['font-family'] = ", ".join(
                dict.fromkeys(_get_all_quoted_names(prop))
                )

            if prop.get_stretch() != 'normal':
                font_style['font-stretch'] = prop.get_stretch()
            attrib['style'] = _generate_css({**font_style, **color_style})

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
                font_style['text-anchor'] = ha_mpl_to_svg[mtext.get_ha()]

                attrib['x'] = _short_float_fmt(ax)
                attrib['y'] = _short_float_fmt(ay)
                attrib['style'] = _generate_css({**font_style, **color_style})
                attrib['transform'] = _generate_transform([
                    ("rotate", (-angle, ax, ay))])

            else:
                attrib['transform'] = _generate_transform([
                    ('translate', (x, y)),
                    ('rotate', (-angle,))])

            writer.element('text', s, attrib=attrib)

        else:
            writer.comment(s)

            width, height, descent, glyphs, rects = \
                self._text2path.mathtext_parser.parse(s, 72, prop)

            # Apply attributes to 'g', not 'text', because we likely have some
            # rectangles as well with the same style and transformation.
            writer.start('g',
                         style=_generate_css({**font_style, **color_style}),
                         transform=_generate_transform([
                             ('translate', (x, y)),
                             ('rotate', (-angle,))]),
                         )

            writer.start('text')

            # Sort the characters by font, and output one tspan for each.
            spans = {}
            for font, fontsize, thetext, new_x, new_y in glyphs:
                entry = fm.ttfFontProperty(font)
                font_style = {}
                # Separate font style in its separate attributes
                if entry.style != 'normal':
                    font_style['font-style'] = entry.style
                if entry.variant != 'normal':
                    font_style['font-variant'] = entry.variant
                if entry.weight != 400:
                    font_style['font-weight'] = f'{entry.weight}'
                font_style['font-size'] = f'{_short_float_fmt(fontsize)}px'
                font_style['font-family'] = f'{entry.name!r}'  # ensure quoting
                if entry.stretch != 'normal':
                    font_style['font-stretch'] = entry.stretch
                style = _generate_css({**font_style, **color_style})
                if thetext == 32:
                    thetext = 0xa0  # non-breaking space
                spans.setdefault(style, []).append((new_x, -new_y, thetext))

            for style, chars in spans.items():
                chars.sort()  # Sort by increasing x position
                for x, y, t in chars:  # Output one tspan for each character
                    writer.element(
                        'tspan',
                        chr(t),
                        x=_short_float_fmt(x),
                        y=_short_float_fmt(y),
                        style=style)

            writer.end('text')

            for x, y, width, height in rects:
                writer.element(
                    'rect',
                    x=_short_float_fmt(x),
                    y=_short_float_fmt(-y-1),
                    width=_short_float_fmt(width),
                    height=_short_float_fmt(height)
                    )

            writer.end('g')
