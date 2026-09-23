    def symmetric_difference(self, other, result_name=None, sort=True):
        """
        Compute the symmetric difference of two Index objects.

        Parameters
        ----------
        other : Index or array-like
        result_name : str
        sort : bool, default True
            Sort the resulting index if possible

            .. versionadded:: 0.24.0

        Returns
        -------
        symmetric_difference : Index

        Notes
        -----
        ``symmetric_difference`` contains elements that appear in either
        ``idx1`` or ``idx2`` but not both. Equivalent to the Index created by
        ``idx1.difference(idx2) | idx2.difference(idx1)`` with duplicates
        dropped.

        Examples
        --------
        >>> idx1 = pd.Index([1, 2, 3, 4])
        >>> idx2 = pd.Index([2, 3, 4, 5])
        >>> idx1.symmetric_difference(idx2)
        Int64Index([1, 5], dtype='int64')

        You can also use the ``^`` operator:

        >>> idx1 ^ idx2
        Int64Index([1, 5], dtype='int64')
        """
        self._assert_can_do_setop(other)
        other, result_name_update = self._convert_can_do_setop(other)
        if result_name is None:
            result_name = result_name_update

        this = self._get_unique_index()
        other = other._get_unique_index()
        indexer = this.get_indexer(other)

        # {this} minus {other}
        common_indexer = indexer.take((indexer != -1).nonzero()[0])
        left_indexer = np.setdiff1d(np.arange(this.size), common_indexer,
                                    assume_unique=True)
        left_diff = this.values.take(left_indexer)

        # {other} minus {this}
        right_indexer = (indexer == -1).nonzero()[0]
        right_diff = other.values.take(right_indexer)

        the_diff = _concat._concat_compat([left_diff, right_diff])
        if sort:
            try:
                the_diff = sorting.safe_sort(the_diff)
            except TypeError:
                pass

        attribs = self._get_attributes_dict()
        attribs['name'] = result_name
        if 'freq' in attribs:
            attribs['freq'] = None
        return self._shallow_copy_with_infer(the_diff, **attribs)
