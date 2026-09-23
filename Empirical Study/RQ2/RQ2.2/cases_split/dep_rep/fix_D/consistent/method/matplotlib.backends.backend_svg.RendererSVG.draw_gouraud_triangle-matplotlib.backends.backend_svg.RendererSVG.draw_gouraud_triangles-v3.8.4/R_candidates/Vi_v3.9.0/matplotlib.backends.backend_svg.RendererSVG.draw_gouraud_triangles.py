    def draw_gouraud_triangles(self, gc, triangles_array, colors_array,
                               transform):
        writer = self.writer
        writer.start('g', **self._get_clip_attrs(gc))
        transform = transform.frozen()
        trans_and_flip = self._make_flip_transform(transform)

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
                values='1 0 0 0 0 \n0 1 0 0 0 \n0 0 1 0 0 \n1 1 1 1 0 \n0 0 0 0 1 ')
            writer.end('filter')

        for points, colors in zip(triangles_array, colors_array):
            self._draw_gouraud_triangle(trans_and_flip.transform(points), colors)
        writer.end('g')
