    @property
    def is_bounded_0_1(self):
        """
        Returns a boolean indicating if the function is bounded
        in the [0-1 interval].

        """
        return self._func.is_bounded_0_1()
