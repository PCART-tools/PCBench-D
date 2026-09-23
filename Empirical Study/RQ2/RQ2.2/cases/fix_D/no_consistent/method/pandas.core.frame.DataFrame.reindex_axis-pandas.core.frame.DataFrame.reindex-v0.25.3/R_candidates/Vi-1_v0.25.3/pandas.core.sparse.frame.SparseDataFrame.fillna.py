    def fillna(
        self, value=None, method=None, axis=0, inplace=False, limit=None, downcast=None
    ):
        new_self = super().fillna(
            value=value,
            method=method,
            axis=axis,
            inplace=inplace,
            limit=limit,
            downcast=downcast,
        )
        if not inplace:
            self = new_self

        # set the fill value if we are filling as a scalar with nothing special
        # going on
        if value is not None and value == value and method is None and limit is None:
            self._default_fill_value = value

        if not inplace:
            return self
