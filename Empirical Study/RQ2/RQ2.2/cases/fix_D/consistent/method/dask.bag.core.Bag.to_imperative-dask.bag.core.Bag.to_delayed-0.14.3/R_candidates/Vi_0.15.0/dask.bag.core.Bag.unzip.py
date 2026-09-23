    def unzip(self, n):
        """Transform a bag of tuples to ``n`` bags of their elements.

        Examples
        --------
        >>> b = from_sequence([(i, i + 1, i + 2) for i in range(10)])
        >>> first, second, third = b.unzip(3)
        >>> isinstance(first, Bag)
        True
        >>> first.compute()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        Note that this is equivalent to:

        >>> first, second, third = (b.pluck(i) for i in range(3))
        """
        return tuple(self.pluck(i) for i in range(n))
