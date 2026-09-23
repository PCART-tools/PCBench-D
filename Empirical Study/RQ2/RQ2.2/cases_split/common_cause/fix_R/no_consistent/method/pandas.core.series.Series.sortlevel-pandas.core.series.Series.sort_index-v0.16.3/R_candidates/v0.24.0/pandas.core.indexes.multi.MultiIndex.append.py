    def append(self, other):
        """
        Append a collection of Index options together

        Parameters
        ----------
        other : Index or list/tuple of indices

        Returns
        -------
        appended : Index
        """
        if not isinstance(other, (list, tuple)):
            other = [other]

        if all((isinstance(o, MultiIndex) and o.nlevels >= self.nlevels)
               for o in other):
            arrays = []
            for i in range(self.nlevels):
                label = self._get_level_values(i)
                appended = [o._get_level_values(i) for o in other]
                arrays.append(label.append(appended))
            return MultiIndex.from_arrays(arrays, names=self.names)

        to_concat = (self.values, ) + tuple(k._values for k in other)
        new_tuples = np.concatenate(to_concat)

        # if all(isinstance(x, MultiIndex) for x in other):
        try:
            return MultiIndex.from_tuples(new_tuples, names=self.names)
        except (TypeError, IndexError):
            return Index(new_tuples)
