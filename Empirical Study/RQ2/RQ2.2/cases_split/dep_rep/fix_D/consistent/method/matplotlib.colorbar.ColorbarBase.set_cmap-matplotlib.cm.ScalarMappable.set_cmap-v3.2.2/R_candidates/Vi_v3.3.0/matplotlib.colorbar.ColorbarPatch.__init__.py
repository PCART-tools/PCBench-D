    def __init__(self, ax, mappable, **kw):
        # we do not want to override the behaviour of solids
        # so add a new attribute which will be a list of the
        # colored patches in the colorbar
        self.solids_patches = []
        Colorbar.__init__(self, ax, mappable, **kw)
