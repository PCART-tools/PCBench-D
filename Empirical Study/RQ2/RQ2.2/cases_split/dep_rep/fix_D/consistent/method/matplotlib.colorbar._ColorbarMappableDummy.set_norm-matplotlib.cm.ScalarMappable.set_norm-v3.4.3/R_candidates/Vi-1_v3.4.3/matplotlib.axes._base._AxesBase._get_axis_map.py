    def _get_axis_map(self):
        """
        Return a mapping of `Axis` "names" to `Axis` instances.

        The `Axis` name is derived from the attribute under which the instance
        is stored, so e.g. for polar axes, the theta-axis is still named "x"
        and the r-axis is still named "y" (for back-compatibility).

        In practice, this means that the entries are typically "x" and "y", and
        additionally "z" for 3D axes.
        """
        d = {}
        axis_list = self._get_axis_list()
        for k, v in vars(self).items():
            if k.endswith("axis") and v in axis_list:
                d[k[:-len("axis")]] = v
        return d
