    def get_axes(self):
        """
        Return a list of Axes in the SubFigure. You can access and modify the
        Axes in the Figure through this list.

        Do not modify the list itself. Instead, use `~.SubFigure.add_axes`,
        `~.SubFigure.add_subplot` or `~.SubFigure.delaxes` to add or remove an
        Axes.

        Note: This is equivalent to the property `~.SubFigure.axes`.
        """
        return self._localaxes.as_list()
