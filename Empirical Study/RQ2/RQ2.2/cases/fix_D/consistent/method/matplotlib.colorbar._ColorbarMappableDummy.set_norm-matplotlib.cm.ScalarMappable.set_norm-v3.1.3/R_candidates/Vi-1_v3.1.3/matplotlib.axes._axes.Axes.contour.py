    @_preprocess_data()
    def contour(self, *args, **kwargs):
        kwargs['filled'] = False
        contours = mcontour.QuadContourSet(self, *args, **kwargs)
        self.autoscale_view()
        return contours
