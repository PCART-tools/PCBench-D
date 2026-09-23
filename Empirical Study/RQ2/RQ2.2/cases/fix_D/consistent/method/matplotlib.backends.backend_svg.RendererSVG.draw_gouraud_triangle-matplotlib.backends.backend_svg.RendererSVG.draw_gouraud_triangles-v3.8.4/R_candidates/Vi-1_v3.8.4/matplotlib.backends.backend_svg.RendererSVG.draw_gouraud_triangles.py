    def draw_gouraud_triangles(self, gc, triangles_array, colors_array,
                               transform):
        self.writer.start('g', **self._get_clip_attrs(gc))
        transform = transform.frozen()
        for tri, col in zip(triangles_array, colors_array):
            self._draw_gouraud_triangle(gc, tri, col, transform)
        self.writer.end('g')
