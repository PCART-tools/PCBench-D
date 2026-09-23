    def __init__(self, child):
        """
        *child*: A `Transform` instance.  This child may later
        be replaced with :meth:`set`.
        """
        _api.check_isinstance(Transform, child=child)
        super().__init__()
        self.set(child)
