    @final
    def _get_merge_keys(
        self,
    ) -> tuple[
        list[ArrayLike],
        list[ArrayLike],
        list[Hashable],
        list[Hashable],
        list[Hashable],
    ]:
        """
        Returns
        -------
        left_keys, right_keys, join_names, left_drop, right_drop
        """
        left_keys: list[ArrayLike] = []
        right_keys: list[ArrayLike] = []
        join_names: list[Hashable] = []
        right_drop: list[Hashable] = []
        left_drop: list[Hashable] = []

        left, right = self.left, self.right

        is_lkey = lambda x: isinstance(x, _known) and len(x) == len(left)
        is_rkey = lambda x: isinstance(x, _known) and len(x) == len(right)

        # Note that pd.merge_asof() has separate 'on' and 'by' parameters. A
        # user could, for example, request 'left_index' and 'left_by'. In a
        # regular pd.merge(), users cannot specify both 'left_index' and
        # 'left_on'. (Instead, users have a MultiIndex). That means the
        # self.left_on in this function is always empty in a pd.merge(), but
        # a pd.merge_asof(left_index=True, left_by=...) will result in a
        # self.left_on array with a None in the middle of it. This requires
        # a work-around as designated in the code below.
        # See _validate_left_right_on() for where this happens.

        # ugh, spaghetti re #733
        if _any(self.left_on) and _any(self.right_on):
            for lk, rk in zip(self.left_on, self.right_on):
                lk = extract_array(lk, extract_numpy=True)
                rk = extract_array(rk, extract_numpy=True)
                if is_lkey(lk):
                    lk = cast(ArrayLike, lk)
                    left_keys.append(lk)
                    if is_rkey(rk):
                        rk = cast(ArrayLike, rk)
                        right_keys.append(rk)
                        join_names.append(None)  # what to do?
                    else:
                        # Then we're either Hashable or a wrong-length arraylike,
                        #  the latter of which will raise
                        rk = cast(Hashable, rk)
                        if rk is not None:
                            right_keys.append(right._get_label_or_level_values(rk))
                            join_names.append(rk)
                        else:
                            # work-around for merge_asof(right_index=True)
                            right_keys.append(right.index._values)
                            join_names.append(right.index.name)
                else:
                    if not is_rkey(rk):
                        # Then we're either Hashable or a wrong-length arraylike,
                        #  the latter of which will raise
                        rk = cast(Hashable, rk)
                        if rk is not None:
                            right_keys.append(right._get_label_or_level_values(rk))
                        else:
                            # work-around for merge_asof(right_index=True)
                            right_keys.append(right.index._values)
                        if lk is not None and lk == rk:  # FIXME: what about other NAs?
                            # avoid key upcast in corner case (length-0)
                            lk = cast(Hashable, lk)
                            if len(left) > 0:
                                right_drop.append(rk)
                            else:
                                left_drop.append(lk)
                    else:
                        rk = cast(ArrayLike, rk)
                        right_keys.append(rk)
                    if lk is not None:
                        # Then we're either Hashable or a wrong-length arraylike,
                        #  the latter of which will raise
                        lk = cast(Hashable, lk)
                        left_keys.append(left._get_label_or_level_values(lk))
                        join_names.append(lk)
                    else:
                        # work-around for merge_asof(left_index=True)
                        left_keys.append(left.index._values)
                        join_names.append(left.index.name)
        elif _any(self.left_on):
            for k in self.left_on:
                if is_lkey(k):
                    k = extract_array(k, extract_numpy=True)
                    k = cast(ArrayLike, k)
                    left_keys.append(k)
                    join_names.append(None)
                else:
                    # Then we're either Hashable or a wrong-length arraylike,
                    #  the latter of which will raise
                    k = cast(Hashable, k)
                    left_keys.append(left._get_label_or_level_values(k))
                    join_names.append(k)
            if isinstance(self.right.index, MultiIndex):
                right_keys = [
                    lev._values.take(lev_codes)
                    for lev, lev_codes in zip(
                        self.right.index.levels, self.right.index.codes
                    )
                ]
            else:
                right_keys = [self.right.index._values]
        elif _any(self.right_on):
            for k in self.right_on:
                k = extract_array(k, extract_numpy=True)
                if is_rkey(k):
                    k = cast(ArrayLike, k)
                    right_keys.append(k)
                    join_names.append(None)
                else:
                    # Then we're either Hashable or a wrong-length arraylike,
                    #  the latter of which will raise
                    k = cast(Hashable, k)
                    right_keys.append(right._get_label_or_level_values(k))
                    join_names.append(k)
            if isinstance(self.left.index, MultiIndex):
                left_keys = [
                    lev._values.take(lev_codes)
                    for lev, lev_codes in zip(
                        self.left.index.levels, self.left.index.codes
                    )
                ]
            else:
                left_keys = [self.left.index._values]

        return left_keys, right_keys, join_names, left_drop, right_drop
