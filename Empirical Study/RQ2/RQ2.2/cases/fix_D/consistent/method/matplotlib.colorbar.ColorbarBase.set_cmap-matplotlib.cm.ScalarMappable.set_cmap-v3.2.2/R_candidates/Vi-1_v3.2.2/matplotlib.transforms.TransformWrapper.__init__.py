    def __init__(self, child):
        """
        *child*: A class:`Transform` instance.  This child may later
        be replaced with :meth:`set`.
        """
        cbook._check_isinstance(Transform, child=child)
        self._init(child)
        self.set_children(child)
