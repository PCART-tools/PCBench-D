    def cleaned(self, transform=None, remove_nans=False, clip=None,
                quantize=False, simplify=False, curves=False,
                stroke_width=1.0, snap=False, sketch=None):
        """
        Cleans up the path according to the parameters returning a new
        Path instance.

        .. seealso::

            See :meth:`iter_segments` for details of the keyword arguments.

        Returns
        -------
        Path instance with cleaned up vertices and codes.

        """
        vertices, codes = _path.cleanup_path(self, transform,
                                             remove_nans, clip,
                                             snap, stroke_width,
                                             simplify, curves, sketch)
        internals = {'should_simplify': self.should_simplify and not simplify,
                     'has_nonfinite': self.has_nonfinite and not remove_nans,
                     'simplify_threshold': self.simplify_threshold,
                     'interpolation_steps': self._interpolation_steps}
        return Path._fast_from_codes_and_verts(vertices, codes, internals)
