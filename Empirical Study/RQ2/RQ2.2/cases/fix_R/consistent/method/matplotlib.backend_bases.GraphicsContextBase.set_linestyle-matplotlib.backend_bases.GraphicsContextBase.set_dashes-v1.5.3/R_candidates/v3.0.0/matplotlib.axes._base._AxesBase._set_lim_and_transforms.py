    def _set_lim_and_transforms(self):
        """
        set the *_xaxis_transform*, *_yaxis_transform*,
        *transScale*, *transData*, *transLimits* and *transAxes*
        transformations.

        .. note::

            This method is primarily used by rectilinear projections
            of the :class:`~matplotlib.axes.Axes` class, and is meant
            to be overridden by new kinds of projection axes that need
            different transformations and limits. (See
            :class:`~matplotlib.projections.polar.PolarAxes` for an
            example.

        """
        self.transAxes = mtransforms.BboxTransformTo(self.bbox)

        # Transforms the x and y axis separately by a scale factor.
        # It is assumed that this part will have non-linear components
        # (e.g., for a log scale).
        self.transScale = mtransforms.TransformWrapper(
            mtransforms.IdentityTransform())

        # An affine transformation on the data, generally to limit the
        # range of the axes
        self.transLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewLim, self.transScale))

        # The parentheses are important for efficiency here -- they
        # group the last two (which are usually affines) separately
        # from the first (which, with log-scaling can be non-affine).
        self.transData = self.transScale + (self.transLimits + self.transAxes)

        self._xaxis_transform = mtransforms.blended_transform_factory(
            self.transData, self.transAxes)
        self._yaxis_transform = mtransforms.blended_transform_factory(
            self.transAxes, self.transData)
