    def _delegate_method(self, name: str, *args, **kwargs):
        raise TypeError(f"You cannot call method {name}")
