    def __init__(
        self,
        index: Index,
        grouper=None,
        obj: NDFrame | None = None,
        level=None,
        sort: bool = True,
        observed: bool = False,
        in_axis: bool = False,
        dropna: bool = True,
        uniques: ArrayLike | None = None,
    ) -> None:
        self.level = level
        self._orig_grouper = grouper
        grouping_vector = _convert_grouper(index, grouper)
        self._all_grouper = None
        self._orig_cats = None
        self._index = index
        self._sort = sort
        self.obj = obj
        self._observed = observed
        self.in_axis = in_axis
        self._dropna = dropna
        self._uniques = uniques

        # we have a single grouper which may be a myriad of things,
        # some of which are dependent on the passing in level

        ilevel = self._ilevel
        if ilevel is not None:
            # In extant tests, the new self.grouping_vector matches
            #  `index.get_level_values(ilevel)` whenever
            #  mapper is None and isinstance(index, MultiIndex)
            if isinstance(index, MultiIndex):
                index_level = index.get_level_values(ilevel)
            else:
                index_level = index

            if grouping_vector is None:
                grouping_vector = index_level
            else:
                mapper = grouping_vector
                grouping_vector = index_level.map(mapper)

        # a passed Grouper like, directly get the grouper in the same way
        # as single grouper groupby, use the group_info to get codes
        elif isinstance(grouping_vector, Grouper):
            # get the new grouper; we already have disambiguated
            # what key/level refer to exactly, don't need to
            # check again as we have by this point converted these
            # to an actual value (rather than a pd.Grouper)
            assert self.obj is not None  # for mypy
            newgrouper, newobj = grouping_vector._get_grouper(self.obj, validate=False)
            self.obj = newobj

            if isinstance(newgrouper, ops.BinGrouper):
                # TODO: can we unwrap this and get a tighter typing
                #  for self.grouping_vector?
                grouping_vector = newgrouper
            else:
                # ops.BaseGrouper
                # TODO: 2023-02-03 no test cases with len(newgrouper.groupings) > 1.
                #  If that were to occur, would we be throwing out information?
                # error: Cannot determine type of "grouping_vector"  [has-type]
                ng = newgrouper.groupings[0].grouping_vector  # type: ignore[has-type]
                # use Index instead of ndarray so we can recover the name
                grouping_vector = Index(ng, name=newgrouper.result_index.name)

        elif not isinstance(
            grouping_vector, (Series, Index, ExtensionArray, np.ndarray)
        ):
            # no level passed
            if getattr(grouping_vector, "ndim", 1) != 1:
                t = str(type(grouping_vector))
                raise ValueError(f"Grouper for '{t}' not 1-dimensional")

            grouping_vector = index.map(grouping_vector)

            if not (
                hasattr(grouping_vector, "__len__")
                and len(grouping_vector) == len(index)
            ):
                grper = pprint_thing(grouping_vector)
                errmsg = (
                    "Grouper result violates len(labels) == "
                    f"len(data)\nresult: {grper}"
                )
                raise AssertionError(errmsg)

        if isinstance(grouping_vector, np.ndarray):
            if grouping_vector.dtype.kind in ["m", "M"]:
                # if we have a date/time-like grouper, make sure that we have
                # Timestamps like
                # TODO 2022-10-08 we only have one test that gets here and
                #  values are already in nanoseconds in that case.
                grouping_vector = Series(grouping_vector).to_numpy()
        elif is_categorical_dtype(grouping_vector):
            # a passed Categorical
            self._orig_cats = grouping_vector.categories
            grouping_vector, self._all_grouper = recode_for_groupby(
                grouping_vector, sort, observed
            )

        self.grouping_vector = grouping_vector
