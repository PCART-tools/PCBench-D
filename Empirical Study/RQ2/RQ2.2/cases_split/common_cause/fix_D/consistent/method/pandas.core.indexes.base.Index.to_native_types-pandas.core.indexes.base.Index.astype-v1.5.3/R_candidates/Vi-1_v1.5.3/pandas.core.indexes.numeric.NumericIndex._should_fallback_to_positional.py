    @cache_readonly  # type: ignore[misc]
    @doc(Index._should_fallback_to_positional)
    def _should_fallback_to_positional(self) -> bool:
        return False
