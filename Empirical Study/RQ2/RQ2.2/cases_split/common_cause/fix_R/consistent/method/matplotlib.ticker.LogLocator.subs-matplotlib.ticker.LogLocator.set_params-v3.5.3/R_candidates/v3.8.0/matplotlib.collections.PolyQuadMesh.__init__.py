    def __init__(self, coordinates, **kwargs):
        # We need to keep track of whether we are using deprecated compression
        # Update it after the initializers
        self._deprecated_compression = False
        super().__init__(coordinates=coordinates)
        PolyCollection.__init__(self, verts=[], **kwargs)
        # Store this during the compression deprecation period
        self._original_mask = ~self._get_unmasked_polys()
        self._deprecated_compression = np.any(self._original_mask)
        # Setting the verts updates the paths of the PolyCollection
        # This is called after the initializers to make sure the kwargs
        # have all been processed and available for the masking calculations
        self._set_unmasked_verts()
