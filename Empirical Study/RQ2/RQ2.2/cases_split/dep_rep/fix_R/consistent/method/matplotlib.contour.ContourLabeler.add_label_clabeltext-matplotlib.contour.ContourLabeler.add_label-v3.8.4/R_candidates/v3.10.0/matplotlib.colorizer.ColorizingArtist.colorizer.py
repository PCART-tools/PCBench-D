    @colorizer.setter
    def colorizer(self, cl):
        _api.check_isinstance(Colorizer, colorizer=cl)
        self._colorizer.callbacks.disconnect(self._id_colorizer)
        self._colorizer = cl
        self._id_colorizer = cl.callbacks.connect('changed', self.changed)
