    @classmethod
    def linear_spine(cls, axes, spine_type, **kwargs):
        """
        (staticmethod) Returns a linear :class:`Spine`.
        """
        # all values of 13 get replaced upon call to set_bounds()
        if spine_type == 'left':
            path = mpath.Path([(0.0, 13), (0.0, 13)])
        elif spine_type == 'right':
            path = mpath.Path([(1.0, 13), (1.0, 13)])
        elif spine_type == 'bottom':
            path = mpath.Path([(13, 0.0), (13, 0.0)])
        elif spine_type == 'top':
            path = mpath.Path([(13, 1.0), (13, 1.0)])
        else:
            raise ValueError('unable to make path for spine "%s"' % spine_type)
        result = cls(axes, spine_type, path, **kwargs)
        result.set_visible(rcParams['axes.spines.{0}'.format(spine_type)])

        return result
