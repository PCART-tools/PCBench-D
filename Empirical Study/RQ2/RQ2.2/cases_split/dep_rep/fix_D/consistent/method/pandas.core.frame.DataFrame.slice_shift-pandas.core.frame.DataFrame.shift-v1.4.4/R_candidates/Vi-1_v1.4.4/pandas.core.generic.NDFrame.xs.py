    @final
    def xs(self, key, axis=0, level=None, drop_level: bool_t = True):
        """
        Return cross-section from the Series/DataFrame.

        This method takes a `key` argument to select data at a particular
        level of a MultiIndex.

        Parameters
        ----------
        key : label or tuple of label
            Label contained in the index, or partially in a MultiIndex.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Axis to retrieve cross-section on.
        level : object, defaults to first n levels (n=1 or len(key))
            In case of a key partially contained in a MultiIndex, indicate
            which levels are used. Levels can be referred by label or position.
        drop_level : bool, default True
            If False, returns object with same levels as self.

        Returns
        -------
        Series or DataFrame
            Cross-section from the original Series or DataFrame
            corresponding to the selected index levels.

        See Also
        --------
        DataFrame.loc : Access a group of rows and columns
            by label(s) or a boolean array.
        DataFrame.iloc : Purely integer-location based indexing
            for selection by position.

        Notes
        -----
        `xs` can not be used to set values.

        MultiIndex Slicers is a generic way to get/set values on
        any level or levels.
        It is a superset of `xs` functionality, see
        :ref:`MultiIndex Slicers <advanced.mi_slicers>`.

        Examples
        --------
        >>> d = {'num_legs': [4, 4, 2, 2],
        ...      'num_wings': [0, 0, 2, 2],
        ...      'class': ['mammal', 'mammal', 'mammal', 'bird'],
        ...      'animal': ['cat', 'dog', 'bat', 'penguin'],
        ...      'locomotion': ['walks', 'walks', 'flies', 'walks']}
        >>> df = pd.DataFrame(data=d)
        >>> df = df.set_index(['class', 'animal', 'locomotion'])
        >>> df
                                   num_legs  num_wings
        class  animal  locomotion
        mammal cat     walks              4          0
               dog     walks              4          0
               bat     flies              2          2
        bird   penguin walks              2          2

        Get values at specified index

        >>> df.xs('mammal')
                           num_legs  num_wings
        animal locomotion
        cat    walks              4          0
        dog    walks              4          0
        bat    flies              2          2

        Get values at several indexes

        >>> df.xs(('mammal', 'dog'))
                    num_legs  num_wings
        locomotion
        walks              4          0

        Get values at specified index and level

        >>> df.xs('cat', level=1)
                           num_legs  num_wings
        class  locomotion
        mammal walks              4          0

        Get values at several indexes and levels

        >>> df.xs(('bird', 'walks'),
        ...       level=[0, 'locomotion'])
                 num_legs  num_wings
        animal
        penguin         2          2

        Get values at specified column and axis

        >>> df.xs('num_wings', axis=1)
        class   animal   locomotion
        mammal  cat      walks         0
                dog      walks         0
                bat      flies         2
        bird    penguin  walks         2
        Name: num_wings, dtype: int64
        """
        axis = self._get_axis_number(axis)
        labels = self._get_axis(axis)

        if isinstance(key, list):
            warnings.warn(
                "Passing lists as key for xs is deprecated and will be removed in a "
                "future version. Pass key as a tuple instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        if level is not None:
            if not isinstance(labels, MultiIndex):
                raise TypeError("Index must be a MultiIndex")
            loc, new_ax = labels.get_loc_level(key, level=level, drop_level=drop_level)

            # create the tuple of the indexer
            _indexer = [slice(None)] * self.ndim
            _indexer[axis] = loc
            indexer = tuple(_indexer)

            result = self.iloc[indexer]
            setattr(result, result._get_axis_name(axis), new_ax)
            return result

        if axis == 1:
            if drop_level:
                return self[key]
            index = self.columns
        else:
            index = self.index

        self._consolidate_inplace()

        if isinstance(index, MultiIndex):
            loc, new_index = index._get_loc_level(key, level=0)
            if not drop_level:
                if lib.is_integer(loc):
                    new_index = index[loc : loc + 1]
                else:
                    new_index = index[loc]
        else:
            loc = index.get_loc(key)

            if isinstance(loc, np.ndarray):
                if loc.dtype == np.bool_:
                    (inds,) = loc.nonzero()
                    return self._take_with_is_copy(inds, axis=axis)
                else:
                    return self._take_with_is_copy(loc, axis=axis)

            if not is_scalar(loc):
                new_index = index[loc]

        if is_scalar(loc) and axis == 0:
            # In this case loc should be an integer
            if self.ndim == 1:
                # if we encounter an array-like and we only have 1 dim
                # that means that their are list/ndarrays inside the Series!
                # so just return them (GH 6394)
                return self._values[loc]

            new_values = self._mgr.fast_xs(loc)

            result = self._constructor_sliced(
                new_values,
                index=self.columns,
                name=self.index[loc],
                dtype=new_values.dtype,
            )
        elif is_scalar(loc):
            result = self.iloc[:, slice(loc, loc + 1)]
        elif axis == 1:
            result = self.iloc[:, loc]
        else:
            result = self.iloc[loc]
            result.index = new_index

        # this could be a view
        # but only in a single-dtyped view sliceable case
        result._set_is_copy(self, copy=not result._is_view)
        return result
