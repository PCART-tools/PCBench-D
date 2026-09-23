    def add(self, a):
        """
        Add Axes *a* to the stack.

        If *a* is already on the stack, don't add it again.
        """
        # All the error checking may be unnecessary; but this method
        # is called so seldom that the overhead is negligible.
        _api.check_isinstance(Axes, a=a)

        if a in self:
            return

        self._ind += 1
        super().push((self._ind, a))
