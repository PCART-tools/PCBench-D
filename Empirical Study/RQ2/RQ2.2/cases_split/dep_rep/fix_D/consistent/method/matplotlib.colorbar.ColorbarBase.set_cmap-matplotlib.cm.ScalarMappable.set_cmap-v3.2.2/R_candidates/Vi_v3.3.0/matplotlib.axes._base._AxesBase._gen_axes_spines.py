    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        """
        Returns
        -------
        dict
            Mapping of spine names to `.Line2D` or `.Patch` instances that are
            used to draw axes spines.

            In the standard axes, spines are single line segments, but in other
            projections they may not be.

        Notes
        -----
        Intended to be overridden by new projection types.
        """
        return OrderedDict((side, mspines.Spine.linear_spine(self, side))
                           for side in ['left', 'right', 'bottom', 'top'])
