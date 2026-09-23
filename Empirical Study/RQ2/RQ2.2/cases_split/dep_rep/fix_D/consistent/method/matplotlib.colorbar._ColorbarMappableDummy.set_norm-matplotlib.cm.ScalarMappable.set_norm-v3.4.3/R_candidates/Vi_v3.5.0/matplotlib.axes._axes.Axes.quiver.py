    @_preprocess_data()
    @docstring.dedent_interpd
    def quiver(self, *args, **kwargs):
        """%(quiver_doc)s"""
        # Make sure units are handled for x and y values
        args = self._quiver_units(args, kwargs)
        q = mquiver.Quiver(self, *args, **kwargs)
        self.add_collection(q, autolim=True)
        self._request_autoscale_view()
        return q
