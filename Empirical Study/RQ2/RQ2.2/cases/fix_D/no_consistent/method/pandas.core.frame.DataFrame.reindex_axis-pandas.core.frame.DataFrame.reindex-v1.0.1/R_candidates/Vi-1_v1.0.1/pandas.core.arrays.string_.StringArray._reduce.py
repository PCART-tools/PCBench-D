    def _reduce(self, name, skipna=True, **kwargs):
        raise TypeError(f"Cannot perform reduction '{name}' with string dtype")
