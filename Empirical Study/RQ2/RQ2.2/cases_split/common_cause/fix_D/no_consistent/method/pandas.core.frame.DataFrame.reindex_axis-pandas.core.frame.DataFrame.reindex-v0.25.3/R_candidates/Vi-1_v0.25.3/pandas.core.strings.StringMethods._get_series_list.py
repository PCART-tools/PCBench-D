    def _get_series_list(self, others, ignore_index=False):
        """
        Auxiliary function for :meth:`str.cat`. Turn potentially mixed input
        into a list of Series (elements without an index must match the length
        of the calling Series/Index).

        Parameters
        ----------
        others : Series, Index, DataFrame, np.ndarray, list-like or list-like
            of objects that are Series, Index or np.ndarray (1-dim)
        ignore_index : boolean, default False
            Determines whether to forcefully align others with index of caller

        Returns
        -------
        tuple : (others transformed into list of Series,
                 boolean whether FutureWarning should be raised)
        """

        # Once str.cat defaults to alignment, this function can be simplified;
        # will not need `ignore_index` and the second boolean output anymore

        from pandas import Index, Series, DataFrame

        # self._orig is either Series or Index
        idx = self._orig if isinstance(self._orig, Index) else self._orig.index

        err_msg = (
            "others must be Series, Index, DataFrame, np.ndarray or "
            "list-like (either containing only strings or containing "
            "only objects of type Series/Index/list-like/np.ndarray)"
        )

        # Generally speaking, all objects without an index inherit the index
        # `idx` of the calling Series/Index - i.e. must have matching length.
        # Objects with an index (i.e. Series/Index/DataFrame) keep their own
        # index, *unless* ignore_index is set to True.
        if isinstance(others, Series):
            warn = not others.index.equals(idx)
            # only reconstruct Series when absolutely necessary
            los = [
                Series(others.values, index=idx) if ignore_index and warn else others
            ]
            return (los, warn)
        elif isinstance(others, Index):
            warn = not others.equals(idx)
            los = [Series(others.values, index=(idx if ignore_index else others))]
            return (los, warn)
        elif isinstance(others, DataFrame):
            warn = not others.index.equals(idx)
            if ignore_index and warn:
                # without copy, this could change "others"
                # that was passed to str.cat
                others = others.copy()
                others.index = idx
            return ([others[x] for x in others], warn)
        elif isinstance(others, np.ndarray) and others.ndim == 2:
            others = DataFrame(others, index=idx)
            return ([others[x] for x in others], False)
        elif is_list_like(others, allow_sets=False):
            others = list(others)  # ensure iterators do not get read twice etc

            # in case of list-like `others`, all elements must be
            # either one-dimensional list-likes or scalars
            if all(is_list_like(x, allow_sets=False) for x in others):
                los = []
                join_warn = False
                depr_warn = False
                # iterate through list and append list of series for each
                # element (which we check to be one-dimensional and non-nested)
                while others:
                    nxt = others.pop(0)  # nxt is guaranteed list-like by above

                    # GH 21950 - DeprecationWarning
                    # only allowing Series/Index/np.ndarray[1-dim] will greatly
                    # simply this function post-deprecation.
                    if not (
                        isinstance(nxt, (Series, Index))
                        or (isinstance(nxt, np.ndarray) and nxt.ndim == 1)
                    ):
                        depr_warn = True

                    if not isinstance(nxt, (DataFrame, Series, Index, np.ndarray)):
                        # safety for non-persistent list-likes (e.g. iterators)
                        # do not map indexed/typed objects; info needed below
                        nxt = list(nxt)

                    # known types for which we can avoid deep inspection
                    no_deep = (
                        isinstance(nxt, np.ndarray) and nxt.ndim == 1
                    ) or isinstance(nxt, (Series, Index))
                    # nested list-likes are forbidden:
                    # -> elements of nxt must not be list-like
                    is_legal = (no_deep and nxt.dtype == object) or all(
                        not is_list_like(x) for x in nxt
                    )

                    # DataFrame is false positive of is_legal
                    # because "x in df" returns column names
                    if not is_legal or isinstance(nxt, DataFrame):
                        raise TypeError(err_msg)

                    nxt, wnx = self._get_series_list(nxt, ignore_index=ignore_index)
                    los = los + nxt
                    join_warn = join_warn or wnx

                if depr_warn:
                    warnings.warn(
                        "list-likes other than Series, Index, or "
                        "np.ndarray WITHIN another list-like are "
                        "deprecated and will be removed in a future "
                        "version.",
                        FutureWarning,
                        stacklevel=4,
                    )
                return (los, join_warn)
            elif all(not is_list_like(x) for x in others):
                return ([Series(others, index=idx)], False)
        raise TypeError(err_msg)
