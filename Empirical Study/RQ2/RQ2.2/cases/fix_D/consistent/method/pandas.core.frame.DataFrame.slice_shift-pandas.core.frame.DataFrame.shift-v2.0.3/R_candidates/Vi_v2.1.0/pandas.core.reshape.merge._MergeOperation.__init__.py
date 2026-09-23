    def __init__(
        self,
        left: DataFrame | Series,
        right: DataFrame | Series,
        how: MergeHow | Literal["asof"] = "inner",
        on: IndexLabel | None = None,
        left_on: IndexLabel | None = None,
        right_on: IndexLabel | None = None,
        left_index: bool = False,
        right_index: bool = False,
        sort: bool = True,
        suffixes: Suffixes = ("_x", "_y"),
        indicator: str | bool = False,
        validate: str | None = None,
    ) -> None:
        _left = _validate_operand(left)
        _right = _validate_operand(right)
        self.left = self.orig_left = _left
        self.right = self.orig_right = _right
        self.how = how

        self.on = com.maybe_make_list(on)

        self.suffixes = suffixes
        self.sort = sort

        self.left_index = left_index
        self.right_index = right_index

        self.indicator = indicator

        if not is_bool(left_index):
            raise ValueError(
                f"left_index parameter must be of type bool, not {type(left_index)}"
            )
        if not is_bool(right_index):
            raise ValueError(
                f"right_index parameter must be of type bool, not {type(right_index)}"
            )

        # GH 40993: raise when merging between different levels; enforced in 2.0
        if _left.columns.nlevels != _right.columns.nlevels:
            msg = (
                "Not allowed to merge between different levels. "
                f"({_left.columns.nlevels} levels on the left, "
                f"{_right.columns.nlevels} on the right)"
            )
            raise MergeError(msg)

        self.left_on, self.right_on = self._validate_left_right_on(left_on, right_on)

        (
            self.left_join_keys,
            self.right_join_keys,
            self.join_names,
            left_drop,
            right_drop,
        ) = self._get_merge_keys()

        if left_drop:
            self.left = self.left._drop_labels_or_levels(left_drop)

        if right_drop:
            self.right = self.right._drop_labels_or_levels(right_drop)

        self._maybe_require_matching_dtypes(self.left_join_keys, self.right_join_keys)
        self._validate_tolerance(self.left_join_keys)

        # validate the merge keys dtypes. We may need to coerce
        # to avoid incompatible dtypes
        self._maybe_coerce_merge_keys()

        # If argument passed to validate,
        # check if columns specified as unique
        # are in fact unique.
        if validate is not None:
            self._validate_validate_kwd(validate)
