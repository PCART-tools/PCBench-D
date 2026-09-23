    def normalize_dictlike_arg(
        self, how: str, obj: DataFrame | Series, func: AggFuncTypeDict
    ) -> AggFuncTypeDict:
        """
        Handler for dict-like argument.

        Ensures that necessary columns exist if obj is a DataFrame, and
        that a nested renamer is not passed. Also normalizes to all lists
        when values consists of a mix of list and non-lists.
        """
        assert how in ("apply", "agg", "transform")

        # Can't use func.values(); wouldn't work for a Series
        if (
            how == "agg"
            and isinstance(obj, ABCSeries)
            and any(is_list_like(v) for _, v in func.items())
        ) or (any(is_dict_like(v) for _, v in func.items())):
            # GH 15931 - deprecation of renaming keys
            raise SpecificationError("nested renamer is not supported")

        if obj.ndim != 1:
            # Check for missing columns on a frame
            cols = set(func.keys()) - set(obj.columns)
            if len(cols) > 0:
                cols_sorted = list(safe_sort(list(cols)))
                raise KeyError(f"Column(s) {cols_sorted} do not exist")

        is_aggregator = lambda x: isinstance(x, (list, tuple, dict))

        # if we have a dict of any non-scalars
        # eg. {'A' : ['mean']}, normalize all to
        # be list-likes
        # Cannot use func.values() because arg may be a Series
        if any(is_aggregator(x) for _, x in func.items()):
            new_func: AggFuncTypeDict = {}
            for k, v in func.items():
                if not is_aggregator(v):
                    # mypy can't realize v is not a list here
                    new_func[k] = [v]  # type:ignore[list-item]
                else:
                    new_func[k] = v
            func = new_func
        return func
