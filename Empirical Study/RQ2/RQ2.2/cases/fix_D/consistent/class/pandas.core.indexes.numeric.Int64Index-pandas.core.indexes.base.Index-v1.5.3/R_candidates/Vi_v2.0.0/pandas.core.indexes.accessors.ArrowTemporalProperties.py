@delegate_names(
    delegate=ArrowExtensionArray,
    accessors=DatetimeArray._datetimelike_ops,
    typ="property",
    accessor_mapping=lambda x: f"_dt_{x}",
    raise_on_missing=False,
)
@delegate_names(
    delegate=ArrowExtensionArray,
    accessors=DatetimeArray._datetimelike_methods,
    typ="method",
    accessor_mapping=lambda x: f"_dt_{x}",
    raise_on_missing=False,
)
class ArrowTemporalProperties(PandasDelegate, PandasObject, NoNewAttributesMixin):
    def __init__(self, data: Series, orig) -> None:
        if not isinstance(data, ABCSeries):
            raise TypeError(
                f"cannot convert an object of type {type(data)} to a datetimelike index"
            )

        self._parent = data
        self._orig = orig
        self._freeze()

    def _delegate_property_get(self, name: str):  # type: ignore[override]
        if not hasattr(self._parent.array, f"_dt_{name}"):
            raise NotImplementedError(
                f"dt.{name} is not supported for {self._parent.dtype}"
            )
        result = getattr(self._parent.array, f"_dt_{name}")

        if not is_list_like(result):
            return result

        if self._orig is not None:
            index = self._orig.index
        else:
            index = self._parent.index
        # return the result as a Series, which is by definition a copy
        result = type(self._parent)(
            result, index=index, name=self._parent.name
        ).__finalize__(self._parent)

        return result

    def _delegate_method(self, name: str, *args, **kwargs):
        if not hasattr(self._parent.array, f"_dt_{name}"):
            raise NotImplementedError(
                f"dt.{name} is not supported for {self._parent.dtype}"
            )

        result = getattr(self._parent.array, f"_dt_{name}")(*args, **kwargs)

        if self._orig is not None:
            index = self._orig.index
        else:
            index = self._parent.index
        # return the result as a Series, which is by definition a copy
        result = type(self._parent)(
            result, index=index, name=self._parent.name
        ).__finalize__(self._parent)

        return result

    def to_pydatetime(self):
        return cast(ArrowExtensionArray, self._parent.array)._dt_to_pydatetime()

    def isocalendar(self):
        from pandas import DataFrame

        result = (
            cast(ArrowExtensionArray, self._parent.array)
            ._dt_isocalendar()
            ._data.combine_chunks()
        )
        iso_calendar_df = DataFrame(
            {
                col: type(self._parent.array)(result.field(i))  # type: ignore[call-arg]
                for i, col in enumerate(["year", "week", "day"])
            }
        )
        return iso_calendar_df
