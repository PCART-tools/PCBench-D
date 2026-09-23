    def isocalendar(self):
        from pandas import DataFrame

        result = (
            cast(ArrowExtensionArray, self._parent.array)
            ._dt_isocalendar()
            ._pa_array.combine_chunks()
        )
        iso_calendar_df = DataFrame(
            {
                col: type(self._parent.array)(result.field(i))  # type: ignore[call-arg]
                for i, col in enumerate(["year", "week", "day"])
            }
        )
        return iso_calendar_df
