    def fillna(
        self, value=None, method=None, limit: int | None = None, copy: bool = True
    ) -> Self:
        if method is not None:
            # view as dt64 so we get treated as timelike in core.missing,
            #  similar to dtl._period_dispatch
            dta = self.view("M8[ns]")
            result = dta.fillna(value=value, method=method, limit=limit, copy=copy)
            # error: Incompatible return value type (got "Union[ExtensionArray,
            # ndarray[Any, Any]]", expected "PeriodArray")
            return result.view(self.dtype)  # type: ignore[return-value]
        return super().fillna(value=value, method=method, limit=limit, copy=copy)
