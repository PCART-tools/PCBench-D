    @Appender(generic._shared_docs['sort_values'] % _shared_doc_kwargs)
    def sort_values(self, axis=0, ascending=True, inplace=False,
                    kind='quicksort', na_position='last'):

        inplace = validate_bool_kwarg(inplace, 'inplace')
        axis = self._get_axis_number(axis)

        # GH 5856/5853
        if inplace and self._is_cached:
            raise ValueError("This Series is a view of some other array, to "
                             "sort in-place you must create a copy")

        def _try_kind_sort(arr):
            # easier to ask forgiveness than permission
            try:
                # if kind==mergesort, it can fail for object dtype
                return arr.argsort(kind=kind)
            except TypeError:
                # stable sort not available for object dtype
                # uses the argsort default quicksort
                return arr.argsort(kind='quicksort')

        arr = self._values
        sortedIdx = np.empty(len(self), dtype=np.int32)

        bad = isnull(arr)

        good = ~bad
        idx = _default_index(len(self))

        argsorted = _try_kind_sort(arr[good])

        if is_list_like(ascending):
            if len(ascending) != 1:
                raise ValueError('Length of ascending (%d) must be 1 '
                                 'for Series' % (len(ascending)))
            ascending = ascending[0]

        if not is_bool(ascending):
            raise ValueError('ascending must be boolean')

        if not ascending:
            argsorted = argsorted[::-1]

        if na_position == 'last':
            n = good.sum()
            sortedIdx[:n] = idx[good][argsorted]
            sortedIdx[n:] = idx[bad]
        elif na_position == 'first':
            n = bad.sum()
            sortedIdx[n:] = idx[good][argsorted]
            sortedIdx[:n] = idx[bad]
        else:
            raise ValueError('invalid na_position: {!r}'.format(na_position))

        result = self._constructor(arr[sortedIdx], index=self.index[sortedIdx])

        if inplace:
            self._update_inplace(result)
        else:
            return result.__finalize__(self)
