    def _fixup(self, value: Any) -> Any:
        try:
            if len(value) == 1 and isinstance(value, tuple):
                return value[0]
        except Exception:
            pass
        return value
