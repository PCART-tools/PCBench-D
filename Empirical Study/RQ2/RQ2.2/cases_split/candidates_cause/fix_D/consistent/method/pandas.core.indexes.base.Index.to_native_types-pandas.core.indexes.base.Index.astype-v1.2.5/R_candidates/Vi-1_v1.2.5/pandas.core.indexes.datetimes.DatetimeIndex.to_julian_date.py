    @doc(DatetimeArray.to_julian_date)
    def to_julian_date(self) -> "Float64Index":
        from pandas.core.indexes.api import Float64Index

        arr = self._data.to_julian_date()
        return Float64Index._simple_new(arr, name=self.name)
