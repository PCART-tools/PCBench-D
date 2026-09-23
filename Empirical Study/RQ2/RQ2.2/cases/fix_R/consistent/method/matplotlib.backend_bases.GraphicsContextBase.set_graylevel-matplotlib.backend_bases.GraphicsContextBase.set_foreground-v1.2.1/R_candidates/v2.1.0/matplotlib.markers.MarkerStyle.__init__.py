    def __init__(self, marker=None, fillstyle=None):
        """
        MarkerStyle

        Attributes
        ----------
        markers : list of known markes

        fillstyles : list of known fillstyles

        filled_markers : list of known filled markers.

        Parameters
        ----------
        marker : string or array_like, optional, default: None
            See the descriptions of possible markers in the module docstring.

        fillstyle : string, optional, default: 'full'
            'full', 'left", 'right', 'bottom', 'top', 'none'
        """
        self._marker_function = None
        self.set_fillstyle(fillstyle)
        self.set_marker(marker)
