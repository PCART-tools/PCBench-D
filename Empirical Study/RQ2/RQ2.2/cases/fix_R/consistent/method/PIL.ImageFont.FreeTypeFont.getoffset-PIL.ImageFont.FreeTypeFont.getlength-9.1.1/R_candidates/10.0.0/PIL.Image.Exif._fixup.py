    def _fixup(self, value):
        try:
            if len(value) == 1 and isinstance(value, tuple):
                return value[0]
        except Exception:
            pass
        return value
