    def fillna(
        self, value, limit=None, inplace: bool = False, downcast=None
    ) -> list[Block]:

        if not self._can_hold_element(value) and self.dtype.kind != "m":
            # We support filling a DatetimeTZ with a `value` whose timezone
            #  is different by coercing to object.
            # TODO: don't special-case td64
            return self.coerce_to_target_dtype(value).fillna(
                value, limit, inplace, downcast
            )

        new_values = self.values.fillna(value=value, limit=limit)
        return [self.make_block_same_class(values=new_values)]
