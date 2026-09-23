    @maybe_split
    def convert(
        self,
        copy: bool = True,
        datetime: bool = True,
        numeric: bool = True,
        timedelta: bool = True,
    ) -> list[Block]:
        """
        attempt to cast any object types to better types return a copy of
        the block (if copy = True) by definition we ARE an ObjectBlock!!!!!
        """
        values = self.values
        if values.ndim == 2:
            # maybe_split ensures we only get here with values.shape[0] == 1,
            # avoid doing .ravel as that might make a copy
            values = values[0]

        res_values = soft_convert_objects(
            values,
            datetime=datetime,
            numeric=numeric,
            timedelta=timedelta,
            copy=copy,
        )
        res_values = ensure_block_shape(res_values, self.ndim)
        return [self.make_block(res_values)]
