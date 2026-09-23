    @artist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        renderer.open_group(self.__class__.__name__, self.get_gid())
        transform = self.get_transform()
        transOffset = self.get_offset_transform()
        offsets = self._offsets

        if self.have_units():
            if len(self._offsets):
                xs = self.convert_xunits(self._offsets[:, 0])
                ys = self.convert_yunits(self._offsets[:, 1])
                offsets = np.column_stack([xs, ys])

        self.update_scalarmappable()

        if not transform.is_affine:
            coordinates = self._coordinates.reshape((-1, 2))
            coordinates = transform.transform(coordinates)
            coordinates = coordinates.reshape(self._coordinates.shape)
            transform = transforms.IdentityTransform()
        else:
            coordinates = self._coordinates

        if not transOffset.is_affine:
            offsets = transOffset.transform_non_affine(offsets)
            transOffset = transOffset.get_affine()

        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_linewidth(self.get_linewidth()[0])

        if self._shading == 'gouraud':
            triangles, colors = self.convert_mesh_to_triangles(
                self._meshWidth, self._meshHeight, coordinates)
            renderer.draw_gouraud_triangles(
                gc, triangles, colors, transform.frozen())
        else:
            renderer.draw_quad_mesh(
                gc, transform.frozen(), self._meshWidth, self._meshHeight,
                coordinates, offsets, transOffset,
                # Backends expect flattened rgba arrays (n*m, 4) for fc and ec
                self.get_facecolor().reshape((-1, 4)),
                self._antialiased, self.get_edgecolors().reshape((-1, 4)))
        gc.restore()
        renderer.close_group(self.__class__.__name__)
        self.stale = False
