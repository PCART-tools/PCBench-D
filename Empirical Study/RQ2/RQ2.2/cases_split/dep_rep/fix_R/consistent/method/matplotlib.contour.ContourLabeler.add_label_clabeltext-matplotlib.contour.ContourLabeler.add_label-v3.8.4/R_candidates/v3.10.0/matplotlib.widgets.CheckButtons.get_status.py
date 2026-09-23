    def get_status(self):
        """
        Return a list of the status (True/False) of all of the check buttons.
        """
        return [not colors.same_color(color, colors.to_rgba("none"))
                for color in self._checks.get_facecolors()]
