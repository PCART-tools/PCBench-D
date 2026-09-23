    @_preprocess_data()
    def contourf(self, *args, **kwargs):
        if not self._hold:
            self.cla()
        kwargs['filled'] = True
        contours = mcontour.QuadContourSet(self, *args, **kwargs)
        self.autoscale_view()
        return contours
