    def __init__(self, marker=None, fillstyle=None):
        """
        Parameters
        ----------
        marker : str, array-like, Path, MarkerStyle, or None, default: None
            - Another instance of *MarkerStyle* copies the details of that
              ``marker``.
            - *None* means no marker.
            - For other possible marker values see the module docstring
              `matplotlib.markers`.

        fillstyle : str, default: :rc:`markers.fillstyle`
            One of 'full', 'left', 'right', 'bottom', 'top', 'none'.
        """
        self._marker_function = None
        self._set_fillstyle(fillstyle)
        self._set_marker(marker)
