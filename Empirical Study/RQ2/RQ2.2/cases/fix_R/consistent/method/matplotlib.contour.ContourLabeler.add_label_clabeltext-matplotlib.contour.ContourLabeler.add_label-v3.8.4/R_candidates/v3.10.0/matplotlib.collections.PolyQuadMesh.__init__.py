    def __init__(self, coordinates, **kwargs):
        super().__init__(coordinates=coordinates)
        PolyCollection.__init__(self, verts=[], **kwargs)
        # Setting the verts updates the paths of the PolyCollection
        # This is called after the initializers to make sure the kwargs
        # have all been processed and available for the masking calculations
        self._set_unmasked_verts()
