    @_preprocess_data()
    def quiver(self, *args, **kw):
        # Make sure units are handled for x and y values
        args = self._quiver_units(args, kw)

        q = mquiver.Quiver(self, *args, **kw)

        self.add_collection(q, autolim=True)
        self.autoscale_view()
        return q
