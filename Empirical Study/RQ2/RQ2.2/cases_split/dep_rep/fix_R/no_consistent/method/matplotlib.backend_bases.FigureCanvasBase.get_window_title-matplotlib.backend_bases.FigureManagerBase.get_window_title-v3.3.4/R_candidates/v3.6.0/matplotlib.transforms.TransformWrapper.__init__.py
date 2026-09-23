    def __init__(self, child):
        """
        *child*: A `Transform` instance.  This child may later
        be replaced with :meth:`set`.
        """
        _api.check_isinstance(Transform, child=child)
        self._init(child)
        self.set_children(child)
