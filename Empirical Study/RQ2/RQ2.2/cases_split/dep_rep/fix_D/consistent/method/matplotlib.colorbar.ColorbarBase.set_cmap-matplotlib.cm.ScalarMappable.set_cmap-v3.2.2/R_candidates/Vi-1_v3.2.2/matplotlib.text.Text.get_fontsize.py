    def get_fontsize(self):
        """
        Return the font size as integer

        See Also
        --------
        .font_manager.FontProperties.get_size_in_points
        """
        return self._fontproperties.get_size_in_points()
