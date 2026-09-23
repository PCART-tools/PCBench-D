    def fillna(
        self, value, limit: int | None = None, inplace: bool = False, downcast=None
    ) -> list[Block]:
        # Caller is responsible for validating limit; if int it is strictly positive

        if self.dtype.kind == "m":
            try:
                res_values = self.values.fillna(value, limit=limit)
            except (ValueError, TypeError):
                # GH#45746
                warnings.warn(
                    "The behavior of fillna with timedelta64[ns] dtype and "
                    f"an incompatible value ({type(value)}) is deprecated. "
                    "In a future version, this will cast to a common dtype "
                    "(usually object) instead of raising, matching the "
                    "behavior of other dtypes.",
                    FutureWarning,
                    stacklevel=find_stack_level(inspect.currentframe()),
                )
                raise
            else:
                res_blk = self.make_block(res_values)
                return [res_blk]

        # TODO: since this now dispatches to super, which in turn dispatches
        #  to putmask, it may *actually* respect 'inplace=True'. If so, add
        #  tests for this.
        return super().fillna(value, limit=limit, inplace=inplace, downcast=downcast)
