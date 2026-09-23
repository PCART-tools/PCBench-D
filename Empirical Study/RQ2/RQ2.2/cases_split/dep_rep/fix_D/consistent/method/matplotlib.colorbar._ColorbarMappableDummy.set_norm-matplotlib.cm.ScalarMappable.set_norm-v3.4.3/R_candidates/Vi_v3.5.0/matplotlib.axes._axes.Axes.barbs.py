    @_preprocess_data()
    @docstring.dedent_interpd
    def barbs(self, *args, **kwargs):
        """%(barbs_doc)s"""
        # Make sure units are handled for x and y values
        args = self._quiver_units(args, kwargs)
        b = mquiver.Barbs(self, *args, **kwargs)
        self.add_collection(b, autolim=True)
        self._request_autoscale_view()
        return b
