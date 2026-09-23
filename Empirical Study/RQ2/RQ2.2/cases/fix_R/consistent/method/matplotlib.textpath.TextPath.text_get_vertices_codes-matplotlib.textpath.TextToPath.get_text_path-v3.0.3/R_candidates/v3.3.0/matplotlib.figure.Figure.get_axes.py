    def get_axes(self):
        """
        Return a list of axes in the Figure. You can access and modify the
        axes in the Figure through this list.

        Do not modify the list itself. Instead, use `~Figure.add_axes`,
        `~.Figure.add_subplot` or `~.Figure.delaxes` to add or remove an axes.

        Note: This is equivalent to the property `~.Figure.axes`.
        """
        return self._axstack.as_list()
