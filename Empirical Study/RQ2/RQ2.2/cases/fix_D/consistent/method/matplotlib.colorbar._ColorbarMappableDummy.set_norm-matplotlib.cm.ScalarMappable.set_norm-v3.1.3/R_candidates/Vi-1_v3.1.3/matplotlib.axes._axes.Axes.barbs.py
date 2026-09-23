    @_preprocess_data()
    @docstring.dedent_interpd
    def barbs(self, *args, **kw):
        """
        %(barbs_doc)s
        """
        # Make sure units are handled for x and y values
        args = self._quiver_units(args, kw)

        b = mquiver.Barbs(self, *args, **kw)
        self.add_collection(b, autolim=True)
        self.autoscale_view()
        return b
