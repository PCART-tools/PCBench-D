    def insert(self, loc: int, item: Hashable, value: ArrayLike, refs=None) -> None:
        """
        Insert item at selected position.

        Parameters
        ----------
        loc : int
        item : hashable
        value : np.ndarray or ExtensionArray
        """
        # insert to the axis; this could possibly raise a TypeError
        new_axis = self.items.insert(loc, item)

        value = extract_array(value, extract_numpy=True)
        if value.ndim == 2:
            if value.shape[0] == 1:
                # error: No overload variant of "__getitem__" of "ExtensionArray"
                # matches argument type "Tuple[int, slice]"
                value = value[0, :]  # type: ignore[call-overload]
            else:
                raise ValueError(
                    f"Expected a 1D array, got an array with shape {value.shape}"
                )
        value = maybe_coerce_values(value)

        # TODO self.arrays can be empty
        # assert len(value) == len(self.arrays[0])

        # TODO is this copy needed?
        arrays = self.arrays.copy()
        arrays.insert(loc, value)

        self.arrays = arrays
        self._axes[1] = new_axis
