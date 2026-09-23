    def __finalize__(self, other, method=None, **kwargs):
        """
        propagate metadata from other to self

        Parameters
        ----------
        other : the object from which to get the attributes that we are going
            to propagate
        method : optional, a passed method name ; possibly to take different
            types of propagation actions based on this

        """
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self
