    @Appender(_index_shared_docs["_shallow_copy"])
    def _shallow_copy(self, values=None, **kwargs):
        if values is None:
            values = self.values
        attributes = self._get_attributes_dict()
        attributes.update(kwargs)
        if not len(values) and "dtype" not in kwargs:
            attributes["dtype"] = self.dtype

        # _simple_new expects an the type of self._data
        values = getattr(values, "_values", values)
        if isinstance(values, ABCDatetimeArray):
            # `self.values` returns `self` for tz-aware, so we need to unwrap
            #  more specifically
            values = values.asi8

        return self._simple_new(values, **attributes)
