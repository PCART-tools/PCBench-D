    def __init__(self, marker=None, fillstyle=None):
        """
        Parameters
        ----------
        marker : str or array-like or None, default: None
            *None* means no marker. For other possible marker values see the
            module docstring `matplotlib.markers`.

        fillstyle : str, default: 'full'
            One of 'full', 'left', 'right', 'bottom', 'top', 'none'.
        """
        self._marker_function = None
        self.set_fillstyle(fillstyle)
        self.set_marker(marker)
