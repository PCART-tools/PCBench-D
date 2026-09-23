    def rename_axis(self, mapper, axis, copy=True, level=None):
        """
        Rename one of axes.

        Parameters
        ----------
        mapper : unary callable
        axis : int
        copy : boolean, default True
        level : int, default None

        """
        obj = self.copy(deep=copy)
        obj.set_axis(axis, _transform_index(self.axes[axis], mapper, level))
        return obj
