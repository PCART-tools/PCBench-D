    @property
    def schema(self) -> OrderedDict[str, DataType]:
        """Get the struct definition as a name/dtype schema dict."""
        if getattr(self, "_s", None) is None:
            return OrderedDict()
        return OrderedDict(self._s.dtype().to_schema())
