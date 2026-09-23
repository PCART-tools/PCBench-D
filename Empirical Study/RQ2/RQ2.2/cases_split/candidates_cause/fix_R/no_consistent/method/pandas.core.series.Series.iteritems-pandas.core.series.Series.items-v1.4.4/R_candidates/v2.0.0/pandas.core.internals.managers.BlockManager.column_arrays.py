    @property
    def column_arrays(self) -> list[np.ndarray]:
        """
        Used in the JSON C code to access column arrays.
        This optimizes compared to using `iget_values` by converting each

        Warning! This doesn't handle Copy-on-Write, so should be used with
        caution (current use case of consuming this in the JSON code is fine).
        """
        # This is an optimized equivalent to
        #  result = [self.iget_values(i) for i in range(len(self.items))]
        result: list[np.ndarray | None] = [None] * len(self.items)

        for blk in self.blocks:
            mgr_locs = blk._mgr_locs
            values = blk.values_for_json()
            if values.ndim == 1:
                # TODO(EA2D): special casing not needed with 2D EAs
                result[mgr_locs[0]] = values

            else:
                for i, loc in enumerate(mgr_locs):
                    result[loc] = values[i]

        # error: Incompatible return value type (got "List[None]",
        # expected "List[ndarray[Any, Any]]")
        return result  # type: ignore[return-value]
