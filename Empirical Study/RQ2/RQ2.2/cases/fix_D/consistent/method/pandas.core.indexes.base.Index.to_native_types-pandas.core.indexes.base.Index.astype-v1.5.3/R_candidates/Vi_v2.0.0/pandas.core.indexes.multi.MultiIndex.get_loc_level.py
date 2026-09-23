    def get_loc_level(self, key, level: IndexLabel = 0, drop_level: bool = True):
        """
        Get location and sliced index for requested label(s)/level(s).

        Parameters
        ----------
        key : label or sequence of labels
        level : int/level name or list thereof, optional
        drop_level : bool, default True
            If ``False``, the resulting index will not drop any level.

        Returns
        -------
        tuple
            A 2-tuple where the elements :

            Element 0: int, slice object or boolean array.

            Element 1: The resulting sliced multiindex/index. If the key
            contains all levels, this will be ``None``.

        See Also
        --------
        MultiIndex.get_loc  : Get location for a label or a tuple of labels.
        MultiIndex.get_locs : Get location for a label/slice/list/mask or a
                              sequence of such.

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([list('abb'), list('def')],
        ...                                names=['A', 'B'])

        >>> mi.get_loc_level('b')
        (slice(1, 3, None), Index(['e', 'f'], dtype='object', name='B'))

        >>> mi.get_loc_level('e', level='B')
        (array([False,  True, False]), Index(['b'], dtype='object', name='A'))

        >>> mi.get_loc_level(['b', 'e'])
        (1, None)
        """
        if not isinstance(level, (list, tuple)):
            level = self._get_level_number(level)
        else:
            level = [self._get_level_number(lev) for lev in level]

        loc, mi = self._get_loc_level(key, level=level)
        if not drop_level:
            if lib.is_integer(loc):
                mi = self[loc : loc + 1]
            else:
                mi = self[loc]
        return loc, mi
