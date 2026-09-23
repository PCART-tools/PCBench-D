    def _get_new_axes(self, *, axes_class=None, **kwargs):
        axes = self._axes
        if axes_class is None:
            if isinstance(axes, SubplotBase):
                axes_class = axes._axes_class
            else:
                axes_class = type(axes)
        return axes_class(axes.get_figure(), axes.get_position(original=True),
                          **kwargs)
