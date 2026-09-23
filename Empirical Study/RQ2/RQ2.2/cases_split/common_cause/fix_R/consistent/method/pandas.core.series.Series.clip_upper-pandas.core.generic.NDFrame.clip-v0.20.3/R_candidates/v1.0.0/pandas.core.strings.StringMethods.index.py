    @Appender(
        _shared_docs["index"]
        % dict(
            side="lowest",
            similar="find",
            method="index",
            also="rindex : Return highest indexes in each strings.",
        )
    )
    @forbid_nonstring_types(["bytes"])
    def index(self, sub, start=0, end=None):
        result = str_index(self._parent, sub, start=start, end=end, side="left")
        return self._wrap_result(result, returns_string=False)
