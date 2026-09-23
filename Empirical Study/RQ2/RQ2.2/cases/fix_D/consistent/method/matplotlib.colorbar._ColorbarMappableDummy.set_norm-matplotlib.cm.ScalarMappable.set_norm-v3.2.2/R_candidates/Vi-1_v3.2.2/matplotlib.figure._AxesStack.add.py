    def add(self, key, a):
        """
        Add Axes *a*, with key *key*, to the stack, and return the stack.

        If *key* is unhashable, replace it by a unique, arbitrary object.

        If *a* is already on the stack, don't add it again, but
        return *None*.
        """
        # All the error checking may be unnecessary; but this method
        # is called so seldom that the overhead is negligible.
        cbook._check_isinstance(Axes, a=a)
        try:
            hash(key)
        except TypeError:
            key = object()

        a_existing = self.get(key)
        if a_existing is not None:
            super().remove((key, a_existing))
            cbook._warn_external(
                "key {!r} already existed; Axes is being replaced".format(key))
            # I don't think the above should ever happen.

        if a in self:
            return None
        self._ind += 1
        return super().push((key, (self._ind, a)))
