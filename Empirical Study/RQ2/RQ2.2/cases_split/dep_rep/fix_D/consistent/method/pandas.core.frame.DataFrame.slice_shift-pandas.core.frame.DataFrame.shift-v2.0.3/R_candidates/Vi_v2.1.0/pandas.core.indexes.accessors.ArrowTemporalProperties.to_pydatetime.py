    def to_pydatetime(self):
        # GH#20306
        warnings.warn(
            f"The behavior of {type(self).__name__}.to_pydatetime is deprecated, "
            "in a future version this will return a Series containing python "
            "datetime objects instead of an ndarray. To retain the old behavior, "
            "call `np.array` on the result",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return cast(ArrowExtensionArray, self._parent.array)._dt_to_pydatetime()
