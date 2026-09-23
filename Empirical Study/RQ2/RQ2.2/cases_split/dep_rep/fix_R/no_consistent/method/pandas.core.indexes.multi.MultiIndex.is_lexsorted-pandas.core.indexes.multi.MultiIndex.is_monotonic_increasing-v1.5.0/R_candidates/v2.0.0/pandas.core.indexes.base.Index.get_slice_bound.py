    def get_slice_bound(self, label, side: Literal["left", "right"]) -> int:
        """
        Calculate slice bound that corresponds to given label.

        Returns leftmost (one-past-the-rightmost if ``side=='right'``) position
        of given label.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}

        Returns
        -------
        int
            Index of label.
        """

        if side not in ("left", "right"):
            raise ValueError(
                "Invalid value for side kwarg, must be either "
                f"'left' or 'right': {side}"
            )

        original_label = label

        # For datetime indices label may be a string that has to be converted
        # to datetime boundary according to its resolution.
        label = self._maybe_cast_slice_bound(label, side)

        # we need to look up the label
        try:
            slc = self.get_loc(label)
        except KeyError as err:
            try:
                return self._searchsorted_monotonic(label, side)
            except ValueError:
                # raise the original KeyError
                raise err

        if isinstance(slc, np.ndarray):
            # get_loc may return a boolean array, which
            # is OK as long as they are representable by a slice.
            assert is_bool_dtype(slc.dtype)
            slc = lib.maybe_booleans_to_slice(slc.view("u1"))
            if isinstance(slc, np.ndarray):
                raise KeyError(
                    f"Cannot get {side} slice bound for non-unique "
                    f"label: {repr(original_label)}"
                )

        if isinstance(slc, slice):
            if side == "left":
                return slc.start
            else:
                return slc.stop
        else:
            if side == "right":
                return slc + 1
            else:
                return slc
