    def _prepare_points(self):
        """Point prep for drawing and hit testing"""

        transform = self.get_transform()
        transOffset = self.get_offset_transform()
        offsets = self._offsets
        paths = self.get_paths()

        if self.have_units():
            paths = []
            for path in self.get_paths():
                vertices = path.vertices
                xs, ys = vertices[:, 0], vertices[:, 1]
                xs = self.convert_xunits(xs)
                ys = self.convert_yunits(ys)
                paths.append(mpath.Path(np.column_stack([xs, ys]), path.codes))

            if offsets.size > 0:
                xs = self.convert_xunits(offsets[:, 0])
                ys = self.convert_yunits(offsets[:, 1])
                offsets = np.column_stack([xs, ys])

        if not transform.is_affine:
            paths = [transform.transform_path_non_affine(path)
                     for path in paths]
            transform = transform.get_affine()
        if not transOffset.is_affine:
            offsets = transOffset.transform_non_affine(offsets)
            # This might have changed an ndarray into a masked array.
            transOffset = transOffset.get_affine()

        if isinstance(offsets, np.ma.MaskedArray):
            offsets = offsets.filled(np.nan)
            # Changing from a masked array to nan-filled ndarray
            # is probably most efficient at this point.

        return transform, transOffset, offsets, paths
