    def __init__(self, marker=_unset, fillstyle=None,
                 transform=None, capstyle=None, joinstyle=None):
        """
        Parameters
        ----------
        marker : str, array-like, Path, MarkerStyle, or None
            - Another instance of *MarkerStyle* copies the details of that
              ``marker``.
            - *None* means no marker.  This is the deprecated default.
            - For other possible marker values, see the module docstring
              `matplotlib.markers`.

        fillstyle : str, default: :rc:`markers.fillstyle`
            One of 'full', 'left', 'right', 'bottom', 'top', 'none'.

        transform : transforms.Transform, default: None
            Transform that will be combined with the native transform of the
            marker.

        capstyle : CapStyle, default: None
            Cap style that will override the default cap style of the marker.

        joinstyle : JoinStyle, default: None
            Join style that will override the default join style of the marker.
        """
        self._marker_function = None
        self._user_transform = transform
        self._user_capstyle = capstyle
        self._user_joinstyle = joinstyle
        self._set_fillstyle(fillstyle)
        # Remove _unset and signature rewriting after deprecation elapses.
        if marker is self._unset:
            marker = ""
            _api.warn_deprecated(
                "3.6", message="Calling MarkerStyle() with no parameters is "
                "deprecated since %(since)s; support will be removed "
                "%(removal)s.  Use MarkerStyle('') to construct an empty "
                "MarkerStyle.")
        if marker is None:
            marker = ""
            _api.warn_deprecated(
                "3.6", message="MarkerStyle(None) is deprecated since "
                "%(since)s; support will be removed %(removal)s.  Use "
                "MarkerStyle('') to construct an empty MarkerStyle.")
        self._set_marker(marker)
