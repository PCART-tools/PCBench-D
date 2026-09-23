    @final
    def make_block_same_class(
        self, values, placement: BlockPlacement | None = None
    ) -> Block:
        """Wrap given values in a block of same type as self."""
        if placement is None:
            placement = self._mgr_locs

        if values.dtype.kind in ["m", "M"]:

            new_values = ensure_wrapped_if_datetimelike(values)
            if new_values is not values:
                # TODO(2.0): remove once fastparquet has stopped relying on it
                warnings.warn(
                    "In a future version, Block.make_block_same_class will "
                    "assume that datetime64 and timedelta64 ndarrays have "
                    "already been cast to DatetimeArray and TimedeltaArray, "
                    "respectively.",
                    DeprecationWarning,
                    stacklevel=find_stack_level(),
                )
            values = new_values

        # We assume maybe_coerce_values has already been called
        return type(self)(values, placement=placement, ndim=self.ndim)
