    def draw_gouraud_triangles(self, gc, triangles_array, colors_array,
                               transform):
        attrib = {}
        clipid = self._get_clip(gc)
        if clipid is not None:
            attrib['clip-path'] = 'url(#%s)' % clipid

        self.writer.start('g', attrib=attrib)

        transform = transform.frozen()
        for tri, col in zip(triangles_array, colors_array):
            self.draw_gouraud_triangle(gc, tri, col, transform)

        self.writer.end('g')
