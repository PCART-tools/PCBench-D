    def concat_same_type(self, to_concat, placement=None):
        # need to handle concat([tz1, tz2]) here, since DatetimeArray
        # only handles cases where all the tzs are the same.
        # Instead of placing the condition here, it could also go into the
        # is_uniform_join_units check, but I'm not sure what is better.
        if len({x.dtype for x in to_concat}) > 1:
            values = _concat._concat_datetime([x.values for x in to_concat])
            placement = placement or slice(0, len(values), 1)

            if self.ndim > 1:
                values = np.atleast_2d(values)
            return ObjectBlock(values, ndim=self.ndim, placement=placement)
        return super().concat_same_type(to_concat, placement)
