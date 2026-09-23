    @_preprocess_data(replace_all_args=True, label_namer=None)
    def quiver(self, *args, **kw):
        # Make sure units are handled for x and y values
        args = self._quiver_units(args, kw)

        q = mquiver.Quiver(self, *args, **kw)

        self.add_collection(q, autolim=True)
        self.autoscale_view()
        return q
