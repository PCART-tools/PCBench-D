    @staticmethod
    def GRIDPOINTS(n: int) -> Flags:
        """
        Fine-tune control over number of gridpoints

        :param n: :py:class:`int` in range ``0 <= n <= 255``
        """
        return Flags.NONE | ((n & 0xFF) << 16)
