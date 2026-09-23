    @cache_readonly
    def _should_fallback_to_positional(self) -> bool:
        # integer lookups in Series.__getitem__ are unambiguously
        #  positional in this case
        # error: Item "ExtensionDtype"/"dtype[Any]" of "Union[dtype[Any],
        # ExtensionDtype]" has no attribute "subtype"
        return self.dtype.subtype.kind in "mM"  # type: ignore[union-attr]
