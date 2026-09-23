    def set_linestyle(self, style):
        """
        Set the linestyle to be one of ('solid', 'dashed', 'dashdot',
        'dotted'). These are defined in the rcParams
        `lines.dashed_pattern`, `lines.dashdot_pattern` and
        `lines.dotted_pattern`.  One may also specify customized dash
        styles by providing a tuple of (offset, dash pairs).
        """
        self._linestyle = style
