    def cleaned(self, transform=None, remove_nans=False, clip=None,
                *, simplify=False, curves=False,
                stroke_width=1.0, snap=False, sketch=None):
        """
        Return a new Path with vertices and codes cleaned according to the
        parameters.

        See Also
        --------
        Path.iter_segments : for details of the keyword arguments.
        """
        vertices, codes = _path.cleanup_path(
            self, transform, remove_nans, clip, snap, stroke_width, simplify,
            curves, sketch)
        pth = Path._fast_from_codes_and_verts(vertices, codes, self)
        if not simplify:
            pth._should_simplify = False
        return pth
