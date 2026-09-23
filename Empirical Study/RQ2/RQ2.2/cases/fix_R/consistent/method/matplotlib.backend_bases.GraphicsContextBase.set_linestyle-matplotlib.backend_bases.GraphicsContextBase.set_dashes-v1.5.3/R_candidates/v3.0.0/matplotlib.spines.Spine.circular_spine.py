    @classmethod
    def circular_spine(cls, axes, center, radius, **kwargs):
        """
        (staticmethod) Returns a circular :class:`Spine`.
        """
        path = mpath.Path.unit_circle()
        spine_type = 'circle'
        result = cls(axes, spine_type, path, **kwargs)
        result.set_patch_circle(center, radius)
        return result
