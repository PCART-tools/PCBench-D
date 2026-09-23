    @_preprocess_data()
    @docstring.dedent_interpd
    def contourf(self, *args, **kwargs):
        """
        Plot filled contours.

        Call signature::

            contourf([X, Y,] Z, [levels], **kwargs)
        %(contour_doc)s
        """
        kwargs['filled'] = True
        contours = mcontour.QuadContourSet(self, *args, **kwargs)
        self._request_autoscale_view()
        return contours
