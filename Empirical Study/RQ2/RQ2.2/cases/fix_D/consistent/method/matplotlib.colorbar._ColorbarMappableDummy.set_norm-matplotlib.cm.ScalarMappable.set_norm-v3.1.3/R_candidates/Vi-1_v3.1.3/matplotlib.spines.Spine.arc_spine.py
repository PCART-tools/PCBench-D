    @classmethod
    def arc_spine(cls, axes, spine_type, center, radius, theta1, theta2,
                  **kwargs):
        """
        (classmethod) Returns an arc :class:`Spine`.
        """
        path = mpath.Path.arc(theta1, theta2)
        result = cls(axes, spine_type, path, **kwargs)
        result.set_patch_arc(center, radius, theta1, theta2)
        return result
