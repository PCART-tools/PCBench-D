    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        """
        Returns a dict whose keys are spine names and values are
        Line2D or Patch instances. Each element is used to draw a
        spine of the axes.

        In the standard axes, this is a single line segment, but in
        other projections it may not be.

        .. note::

            Intended to be overridden by new projection types.

        """
        return OrderedDict([
            ('left', mspines.Spine.linear_spine(self, 'left')),
            ('right', mspines.Spine.linear_spine(self, 'right')),
            ('bottom', mspines.Spine.linear_spine(self, 'bottom')),
            ('top', mspines.Spine.linear_spine(self, 'top'))])
