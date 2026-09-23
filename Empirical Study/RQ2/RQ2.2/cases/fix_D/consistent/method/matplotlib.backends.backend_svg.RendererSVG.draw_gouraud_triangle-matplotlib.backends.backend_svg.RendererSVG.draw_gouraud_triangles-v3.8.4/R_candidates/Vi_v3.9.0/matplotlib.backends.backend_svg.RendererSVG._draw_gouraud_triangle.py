    def _draw_gouraud_triangle(self, transformed_points, colors):
        # This uses a method described here:
        #
        #   http://www.svgopen.org/2005/papers/Converting3DFaceToSVG/index.html
        #
        # that uses three overlapping linear gradients to simulate a
        # Gouraud triangle.  Each gradient goes from fully opaque in
        # one corner to fully transparent along the opposite edge.
        # The line between the stop points is perpendicular to the
        # opposite edge.  Underlying these three gradients is a solid
        # triangle whose color is the average of all three points.

        avg_color = np.average(colors, axis=0)
        if avg_color[-1] == 0:
            # Skip fully-transparent triangles
            return

        writer = self.writer
        writer.start('defs')
        for i in range(3):
            x1, y1 = transformed_points[i]
            x2, y2 = transformed_points[(i + 1) % 3]
            x3, y3 = transformed_points[(i + 2) % 3]
            rgba_color = colors[i]

            if x2 == x3:
                xb = x2
                yb = y1
            elif y2 == y3:
                xb = x1
                yb = y2
            else:
                m1 = (y2 - y3) / (x2 - x3)
                b1 = y2 - (m1 * x2)
                m2 = -(1.0 / m1)
                b2 = y1 - (m2 * x1)
                xb = (-b1 + b2) / (m1 - m2)
                yb = m2 * xb + b2

            writer.start(
                'linearGradient',
                id=f"GR{self._n_gradients:x}_{i:d}",
                gradientUnits="userSpaceOnUse",
                x1=_short_float_fmt(x1), y1=_short_float_fmt(y1),
                x2=_short_float_fmt(xb), y2=_short_float_fmt(yb))
            writer.element(
                'stop',
                offset='1',
                style=_generate_css({
                    'stop-color': rgb2hex(avg_color),
                    'stop-opacity': _short_float_fmt(rgba_color[-1])}))
            writer.element(
                'stop',
                offset='0',
                style=_generate_css({'stop-color': rgb2hex(rgba_color),
                                    'stop-opacity': "0"}))

            writer.end('linearGradient')

        writer.end('defs')

        # triangle formation using "path"
        dpath = (f"M {_short_float_fmt(x1)},{_short_float_fmt(y1)}"
                 f" L {_short_float_fmt(x2)},{_short_float_fmt(y2)}"
                 f" {_short_float_fmt(x3)},{_short_float_fmt(y3)} Z")

        writer.element(
            'path',
            attrib={'d': dpath,
                    'fill': rgb2hex(avg_color),
                    'fill-opacity': '1',
                    'shape-rendering': "crispEdges"})

        writer.start(
                'g',
                attrib={'stroke': "none",
                        'stroke-width': "0",
                        'shape-rendering': "crispEdges",
                        'filter': "url(#colorMat)"})

        writer.element(
            'path',
            attrib={'d': dpath,
                    'fill': f'url(#GR{self._n_gradients:x}_0)',
                    'shape-rendering': "crispEdges"})

        writer.element(
            'path',
            attrib={'d': dpath,
                    'fill': f'url(#GR{self._n_gradients:x}_1)',
                    'filter': 'url(#colorAdd)',
                    'shape-rendering': "crispEdges"})

        writer.element(
            'path',
            attrib={'d': dpath,
                    'fill': f'url(#GR{self._n_gradients:x}_2)',
                    'filter': 'url(#colorAdd)',
                    'shape-rendering': "crispEdges"})

        writer.end('g')

        self._n_gradients += 1
