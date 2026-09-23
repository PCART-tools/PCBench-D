    def diff(self, other):
        """
        Compute sorted set difference of two Index objects

        Notes
        -----
        One can do either of these and achieve the same result

        >>> index - index2
        >>> index.diff(index2)

        Returns
        -------
        diff : Index
        """

        if not hasattr(other, '__iter__'):
            raise TypeError('Input must be iterable!')

        if self.equals(other):
            return Index([], name=self.name)

        if not isinstance(other, Index):
            other = np.asarray(other)
            result_name = self.name
        else:
            result_name = self.name if self.name == other.name else None

        theDiff = sorted(set(self) - set(other))
        return Index(theDiff, name=result_name)
