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
                x1=short_float_fmt(x1), y1=short_float_fmt(y1),
                x2=short_float_fmt(xb), y2=short_float_fmt(yb))
            writer.element(
                'stop',
                offset='0',
                style=generate_css({'stop-color': rgb2hex(c),
                                    'stop-opacity': short_float_fmt(c[-1])}))
            writer.element(
                'stop',
                offset='1',
                style=generate_css({'stop-color': rgb2hex(c),
                                    'stop-opacity': "0"}))
            writer.end('linearGradient')

        writer.element(
            'polygon',
            id='GT%x' % self._n_gradients,
            points=" ".join([short_float_fmt(x)
                             for x in (x1, y1, x2, y2, x3, y3)]))
        writer.end('defs')

        avg_color = np.sum(colors[:, :], axis=0) / 3.0
        href = '#GT%x' % self._n_gradients
        writer.element(
            'use',
            attrib={'xlink:href': href,
                    'fill': rgb2hex(avg_color),
                    'fill-opacity': short_float_fmt(avg_color[-1])})
        for i in range(3):
            writer.element(
                'use',
                attrib={'xlink:href': href,
                        'fill': 'url(#GR%x_%d)' % (self._n_gradients, i),
                        'fill-opacity': '1',
                        'filter': 'url(#colorAdd)'})

        self._n_gradients += 1
