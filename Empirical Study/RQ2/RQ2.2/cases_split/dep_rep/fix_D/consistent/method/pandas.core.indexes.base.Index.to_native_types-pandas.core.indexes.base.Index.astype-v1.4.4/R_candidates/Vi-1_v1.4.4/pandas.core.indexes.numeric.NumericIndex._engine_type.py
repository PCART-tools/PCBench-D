    @property
    def _engine_type(self):
        # error: Invalid index type "Union[dtype[Any], ExtensionDtype]" for
        # "Dict[dtype[Any], Type[IndexEngine]]"; expected type "dtype[Any]"
        return self._engine_types[self.dtype]  # type: ignore[index]
