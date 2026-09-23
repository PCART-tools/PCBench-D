    def _validate_specification(self) -> None:
        if self.how == "cross":
            if (
                self.left_index
                or self.right_index
                or self.right_on is not None
                or self.left_on is not None
                or self.on is not None
            ):
                raise MergeError(
                    "Can not pass on, right_on, left_on or set right_index=True or "
                    "left_index=True"
                )
            return
        # Hm, any way to make this logic less complicated??
        elif self.on is None and self.left_on is None and self.right_on is None:

            if self.left_index and self.right_index:
                self.left_on, self.right_on = (), ()
            elif self.left_index:
                raise MergeError("Must pass right_on or right_index=True")
            elif self.right_index:
                raise MergeError("Must pass left_on or left_index=True")
            else:
                # use the common columns
                left_cols = self.left.columns
                right_cols = self.right.columns
                common_cols = left_cols.intersection(right_cols)
                if len(common_cols) == 0:
                    raise MergeError(
                        "No common columns to perform merge on. "
                        f"Merge options: left_on={self.left_on}, "
                        f"right_on={self.right_on}, "
                        f"left_index={self.left_index}, "
                        f"right_index={self.right_index}"
                    )
                if (
                    not left_cols.join(common_cols, how="inner").is_unique
                    or not right_cols.join(common_cols, how="inner").is_unique
                ):
                    raise MergeError(f"Data columns not unique: {repr(common_cols)}")
                self.left_on = self.right_on = common_cols
        elif self.on is not None:
            if self.left_on is not None or self.right_on is not None:
                raise MergeError(
                    'Can only pass argument "on" OR "left_on" '
                    'and "right_on", not a combination of both.'
                )
            if self.left_index or self.right_index:
                raise MergeError(
                    'Can only pass argument "on" OR "left_index" '
                    'and "right_index", not a combination of both.'
                )
            self.left_on = self.right_on = self.on
        elif self.left_on is not None:
            if self.left_index:
                raise MergeError(
                    'Can only pass argument "left_on" OR "left_index" not both.'
                )
            if not self.right_index and self.right_on is None:
                raise MergeError('Must pass "right_on" OR "right_index".')
            n = len(self.left_on)
            if self.right_index:
                if len(self.left_on) != self.right.index.nlevels:
                    raise ValueError(
                        "len(left_on) must equal the number "
                        'of levels in the index of "right"'
                    )
                self.right_on = [None] * n
        elif self.right_on is not None:
            if self.right_index:
                raise MergeError(
                    'Can only pass argument "right_on" OR "right_index" not both.'
                )
            if not self.left_index and self.left_on is None:
                raise MergeError('Must pass "left_on" OR "left_index".')
            n = len(self.right_on)
            if self.left_index:
                if len(self.right_on) != self.left.index.nlevels:
                    raise ValueError(
                        "len(right_on) must equal the number "
                        'of levels in the index of "left"'
                    )
                self.left_on = [None] * n
        if self.how != "cross" and len(self.right_on) != len(self.left_on):
            raise ValueError("len(right_on) must equal len(left_on)")
