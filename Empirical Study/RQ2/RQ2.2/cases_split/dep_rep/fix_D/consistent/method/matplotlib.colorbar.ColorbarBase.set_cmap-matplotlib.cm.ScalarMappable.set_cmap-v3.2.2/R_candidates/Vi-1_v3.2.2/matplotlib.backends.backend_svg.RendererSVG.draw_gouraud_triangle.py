    def draw_gouraud_triangle(self, gc, points, colors, trans):
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

        writer = self.writer
        if not self._has_gouraud:
            self._has_gouraud = True
            writer.start(
                'filter',
                id='colorAdd')
            writer.element(
                'feComposite',
                attrib={'in': 'SourceGraphic'},
                in2='BackgroundImage',
                operator='arithmetic',
                k2="1", k3="1")
            writer.end('filter')
            # feColorMatrix filter to correct opacity
            writer.start(
                'filter',
                id='colorMat')
            writer.element(
                'feColorMatrix',
                attrib={'type': 'matrix'},
                values='1 0 0 0 0 \n0 1 0 0 0 \n0 0 1 0 0' +
                       ' \n1 1 1 1 0 \n0 0 0 0 1 ')
            writer.end('filter')

        avg_color = np.sum(colors[:, :], axis=0) / 3.0
        # Just skip fully-transparent triangles
        if avg_color[-1] == 0.0:
            return

        trans_and_flip = self._make_flip_transform(trans)
        tpoints = trans_and_flip.transform(points)

        writer.start('defs')
        for i in range(3):
            x1, y1 = tpoints[i]
            x2, y2 = tpoints[(i + 1) % 3]
            x3, y3 = tpoints[(i + 2) % 3]
            c = colors[i][:]

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
                id="GR%x_%d" % (self._n_gradients, i),
                gradientUnits="userSpaceOnUse",
                x1=short_float_fmt(x1), y1=short_float_fmt(y1),
                x2=short_float_fmt(xb), y2=short_float_fmt(yb))
            writer.element(
                'stop',
                offset='1',
                style=generate_css({'stop-color': rgb2hex(avg_color),
                                    'stop-opacity': short_float_fmt(c[-1])}))
            writer.element(
                'stop',
                offset='0',
                style=generate_css({'stop-color': rgb2hex(c),
                                    'stop-opacity': "0"}))

            writer.end('linearGradient')

        writer.end('defs')

        # triangle formation using "path"
        dpath = "M " + short_float_fmt(x1)+',' + short_float_fmt(y1)
        dpath += " L " + short_float_fmt(x2) + ',' + short_float_fmt(y2)
        dpath += " " + short_float_fmt(x3) + ',' + short_float_fmt(y3) + " Z"

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
                    'fill': 'url(#GR%x_0)' % self._n_gradients,
                    'shape-rendering': "crispEdges"})

        writer.element(
            'path',
            attrib={'d': dpath,
                    'fill': 'url(#GR%x_1)' % self._n_gradients,
                    'filter': 'url(#colorAdd)',
                    'shape-rendering': "crispEdges"})

        writer.element(
            'path',
            attrib={'d': dpath,
                    'fill': 'url(#GR%x_2)' % self._n_gradients,
                    'filter': 'url(#colorAdd)',
                    'shape-rendering': "crispEdges"})

        writer.end('g')

        self._n_gradients += 1
