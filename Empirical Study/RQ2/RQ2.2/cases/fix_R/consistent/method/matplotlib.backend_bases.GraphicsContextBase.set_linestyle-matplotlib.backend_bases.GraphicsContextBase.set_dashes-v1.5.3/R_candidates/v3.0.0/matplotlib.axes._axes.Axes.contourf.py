    @_preprocess_data()
    def contourf(self, *args, **kwargs):
        kwargs['filled'] = True
        contours = mcontour.QuadContourSet(self, *args, **kwargs)
        self.autoscale_view()
        return contours
