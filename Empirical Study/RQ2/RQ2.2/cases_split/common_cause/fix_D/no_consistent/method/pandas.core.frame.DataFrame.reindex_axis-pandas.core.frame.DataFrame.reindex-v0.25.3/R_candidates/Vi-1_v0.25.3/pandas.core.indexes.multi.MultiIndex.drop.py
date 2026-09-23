    @deprecate_kwarg(old_arg_name="labels", new_arg_name="codes")
    def drop(self, codes, level=None, errors="raise"):
        """
        Make new MultiIndex with passed list of codes deleted

        Parameters
        ----------
        codes : array-like
            Must be a list of tuples
        level : int or level name, default None

        Returns
        -------
        dropped : MultiIndex
        """
        if level is not None:
            return self._drop_from_level(codes, level)

        try:
            if not isinstance(codes, (np.ndarray, Index)):
                codes = com.index_labels_to_array(codes)
            indexer = self.get_indexer(codes)
            mask = indexer == -1
            if mask.any():
                if errors != "ignore":
                    raise ValueError("codes %s not contained in axis" % codes[mask])
        except Exception:
            pass

        inds = []
        for level_codes in codes:
            try:
                loc = self.get_loc(level_codes)
                # get_loc returns either an integer, a slice, or a boolean
                # mask
                if isinstance(loc, int):
                    inds.append(loc)
                elif isinstance(loc, slice):
                    inds.extend(range(loc.start, loc.stop))
                elif com.is_bool_indexer(loc):
                    if self.lexsort_depth == 0:
                        warnings.warn(
                            "dropping on a non-lexsorted multi-index"
                            " without a level parameter may impact "
                            "performance.",
                            PerformanceWarning,
                            stacklevel=3,
                        )
                    loc = loc.nonzero()[0]
                    inds.extend(loc)
                else:
                    msg = "unsupported indexer of type {}".format(type(loc))
                    raise AssertionError(msg)
            except KeyError:
                if errors != "ignore":
                    raise

        return self.delete(inds)
