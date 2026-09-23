    def __reduce__(self):

        # we use a special reduce here because we need
        # to simply set the .tz (and not reinterpret it)

        d = {"data": self._data}
        d.update(self._get_attributes_dict())
        return _new_DatetimeIndex, (type(self), d), None
