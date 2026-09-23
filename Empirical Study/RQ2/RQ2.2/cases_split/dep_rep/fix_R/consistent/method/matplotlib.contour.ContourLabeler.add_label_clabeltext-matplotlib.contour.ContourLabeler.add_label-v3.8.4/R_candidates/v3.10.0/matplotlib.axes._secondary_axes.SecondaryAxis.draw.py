    def draw(self, renderer):
        """
        Draw the secondary Axes.

        Consults the parent Axes for its limits and converts them
        using the converter specified by
        `~.axes._secondary_axes.set_functions` (or *functions*
        parameter when Axes initialized.)
        """
        self._set_lims()
        # this sets the scale in case the parent has set its scale.
        self._set_scale()
        super().draw(renderer)
