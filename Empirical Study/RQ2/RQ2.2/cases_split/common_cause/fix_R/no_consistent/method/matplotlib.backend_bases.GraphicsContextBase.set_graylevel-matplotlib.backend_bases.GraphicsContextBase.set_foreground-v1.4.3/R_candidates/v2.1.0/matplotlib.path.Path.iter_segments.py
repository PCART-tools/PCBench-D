    def iter_segments(self, transform=None, remove_nans=True, clip=None,
                      snap=False, stroke_width=1.0, simplify=None,
                      curves=True, sketch=None):
        """
        Iterates over all of the curve segments in the path.  Each
        iteration returns a 2-tuple (*vertices*, *code*), where
        *vertices* is a sequence of 1 - 3 coordinate pairs, and *code* is
        one of the :class:`Path` codes.

        Additionally, this method can provide a number of standard
        cleanups and conversions to the path.

        Parameters
        ----------
        transform : None or :class:`~matplotlib.transforms.Transform` instance
            If not None, the given affine transformation will
            be applied to the path.
        remove_nans : {False, True}, optional
            If True, will remove all NaNs from the path and
            insert MOVETO commands to skip over them.
        clip : None or sequence, optional
            If not None, must be a four-tuple (x1, y1, x2, y2)
            defining a rectangle in which to clip the path.
        snap : None or bool, optional
            If None, auto-snap to pixels, to reduce
            fuzziness of rectilinear lines.  If True, force snapping, and
            if False, don't snap.
        stroke_width : float, optional
            The width of the stroke being drawn.  Needed
             as a hint for the snapping algorithm.
        simplify : None or bool, optional
            If True, perform simplification, to remove
             vertices that do not affect the appearance of the path.  If
             False, perform no simplification.  If None, use the
             should_simplify member variable.  See also the rcParams
             path.simplify and path.simplify_threshold.
        curves : {True, False}, optional
            If True, curve segments will be returned as curve
            segments.  If False, all curves will be converted to line
            segments.
        sketch : None or sequence, optional
            If not None, must be a 3-tuple of the form
            (scale, length, randomness), representing the sketch
            parameters.
        """
        if not len(self):
            return

        cleaned = self.cleaned(transform=transform,
                               remove_nans=remove_nans, clip=clip,
                               snap=snap, stroke_width=stroke_width,
                               simplify=simplify, curves=curves,
                               sketch=sketch)
        vertices = cleaned.vertices
        codes = cleaned.codes
        len_vertices = vertices.shape[0]

        # Cache these object lookups for performance in the loop.
        NUM_VERTICES_FOR_CODE = self.NUM_VERTICES_FOR_CODE
        STOP = self.STOP

        i = 0
        while i < len_vertices:
            code = codes[i]
            if code == STOP:
                return
            else:
                num_vertices = NUM_VERTICES_FOR_CODE[code]
                curr_vertices = vertices[i:i+num_vertices].flatten()
                yield curr_vertices, code
                i += num_vertices
