    @_preprocess_data()
    @_docstring.interpd
    def contour(self, *args, **kwargs):
        """
        Plot contour lines.

        Call signature::

            contour([X, Y,] Z, /, [levels], **kwargs)

        The arguments *X*, *Y*, *Z* are positional-only.
        %(contour_doc)s
        """
        kwargs['filled'] = False
        contours = mcontour.QuadContourSet(self, *args, **kwargs)
        self._request_autoscale_view()
        return contours
