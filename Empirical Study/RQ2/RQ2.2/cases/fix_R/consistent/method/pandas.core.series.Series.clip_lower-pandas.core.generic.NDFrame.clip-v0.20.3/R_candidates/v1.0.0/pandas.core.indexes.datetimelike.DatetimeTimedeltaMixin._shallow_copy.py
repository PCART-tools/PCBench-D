    def _shallow_copy(self, values=None, **kwargs):
        if values is None:
            values = self._data
        if isinstance(values, type(self)):
            values = values._data

        attributes = self._get_attributes_dict()

        if "freq" not in kwargs and self.freq is not None:
            if isinstance(values, (DatetimeArray, TimedeltaArray)):
                if values.freq is None:
                    del attributes["freq"]

        attributes.update(kwargs)
        return self._simple_new(values, **attributes)
