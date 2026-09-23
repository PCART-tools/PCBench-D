    @artist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        renderer.open_group(self.__class__.__name__)
        transform = self.get_transform()

        # Get a list of triangles and the color at each vertex.
        tri = self._triangulation
        triangles = tri.get_masked_triangles()

        verts = np.stack((tri.x[triangles], tri.y[triangles]), axis=-1)

        self.update_scalarmappable()
        colors = self._facecolors[triangles]

        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_linewidth(self.get_linewidth()[0])
        renderer.draw_gouraud_triangles(gc, verts, colors, transform.frozen())
        gc.restore()
        renderer.close_group(self.__class__.__name__)
