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

        to_concat = [self]

        if isinstance(other, (list, tuple)):
            to_concat = to_concat + list(other)
        else:
            to_concat.append(other)

        for obj in to_concat:
            if not isinstance(obj, Index):
                raise TypeError('all inputs must be Index')

        names = set([obj.name for obj in to_concat])
        name = None if len(names) > 1 else self.name

        if self.is_categorical():
            # if calling index is category, don't check dtype of others
            from pandas.core.indexes.category import CategoricalIndex
            return CategoricalIndex._append_same_dtype(self, to_concat, name)

        typs = _concat.get_dtype_kinds(to_concat)

        if len(typs) == 1:
            return self._append_same_dtype(to_concat, name=name)
        return _concat._concat_index_asobject(to_concat, name=name)
