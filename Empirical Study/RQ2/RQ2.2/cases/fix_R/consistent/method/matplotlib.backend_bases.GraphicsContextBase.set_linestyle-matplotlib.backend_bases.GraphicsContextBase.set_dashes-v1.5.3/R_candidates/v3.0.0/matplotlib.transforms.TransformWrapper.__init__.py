    def __init__(self, child):
        """
        *child*: A class:`Transform` instance.  This child may later
        be replaced with :meth:`set`.
        """
        if not isinstance(child, Transform):
            raise ValueError("'child' must be an instance of "
                             "'matplotlib.transform.Transform'")
        self._init(child)
        self.set_children(child)
