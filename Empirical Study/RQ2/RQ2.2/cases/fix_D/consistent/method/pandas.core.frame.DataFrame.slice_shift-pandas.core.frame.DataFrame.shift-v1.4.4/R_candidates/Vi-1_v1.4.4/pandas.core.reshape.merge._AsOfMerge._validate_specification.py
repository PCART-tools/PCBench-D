    def _validate_specification(self) -> None:
        super()._validate_specification()

        # we only allow on to be a single item for on
        if len(self.left_on) != 1 and not self.left_index:
            raise MergeError("can only asof on a key for left")

        if len(self.right_on) != 1 and not self.right_index:
            raise MergeError("can only asof on a key for right")

        if self.left_index and isinstance(self.left.index, MultiIndex):
            raise MergeError("left can only have one index")

        if self.right_index and isinstance(self.right.index, MultiIndex):
            raise MergeError("right can only have one index")

        # set 'by' columns
        if self.by is not None:
            if self.left_by is not None or self.right_by is not None:
                raise MergeError("Can only pass by OR left_by and right_by")
            self.left_by = self.right_by = self.by
        if self.left_by is None and self.right_by is not None:
            raise MergeError("missing left_by")
        if self.left_by is not None and self.right_by is None:
            raise MergeError("missing right_by")

        # GH#29130 Check that merge keys do not have dtype object
        if not self.left_index:
            left_on = self.left_on[0]
            if is_array_like(left_on):
                lo_dtype = left_on.dtype
            else:
                lo_dtype = (
                    self.left[left_on].dtype
                    if left_on in self.left.columns
                    else self.left.index.get_level_values(left_on)
                )
        else:
            lo_dtype = self.left.index.dtype

        if not self.right_index:
            right_on = self.right_on[0]
            if is_array_like(right_on):
                ro_dtype = right_on.dtype
            else:
                ro_dtype = (
                    self.right[right_on].dtype
                    if right_on in self.right.columns
                    else self.right.index.get_level_values(right_on)
                )
        else:
            ro_dtype = self.right.index.dtype

        if is_object_dtype(lo_dtype) or is_object_dtype(ro_dtype):
            raise MergeError(
                f"Incompatible merge dtype, {repr(ro_dtype)} and "
                f"{repr(lo_dtype)}, both sides must have numeric dtype"
            )

        # add 'by' to our key-list so we can have it in the
        # output as a key
        if self.left_by is not None:
            if not is_list_like(self.left_by):
                self.left_by = [self.left_by]
            if not is_list_like(self.right_by):
                self.right_by = [self.right_by]

            if len(self.left_by) != len(self.right_by):
                raise MergeError("left_by and right_by must be same length")

            self.left_on = self.left_by + list(self.left_on)
            self.right_on = self.right_by + list(self.right_on)

        # check 'direction' is valid
        if self.direction not in ["backward", "forward", "nearest"]:
            raise MergeError(f"direction invalid: {self.direction}")
