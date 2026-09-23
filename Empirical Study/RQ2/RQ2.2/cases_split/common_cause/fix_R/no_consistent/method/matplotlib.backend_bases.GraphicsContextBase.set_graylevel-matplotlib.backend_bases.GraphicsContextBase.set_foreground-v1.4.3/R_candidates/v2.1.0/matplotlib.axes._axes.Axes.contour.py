    @_preprocess_data()
    def contour(self, *args, **kwargs):
        if not self._hold:
            self.cla()
        kwargs['filled'] = False
        contours = mcontour.QuadContourSet(self, *args, **kwargs)
        self.autoscale_view()
        return contours
