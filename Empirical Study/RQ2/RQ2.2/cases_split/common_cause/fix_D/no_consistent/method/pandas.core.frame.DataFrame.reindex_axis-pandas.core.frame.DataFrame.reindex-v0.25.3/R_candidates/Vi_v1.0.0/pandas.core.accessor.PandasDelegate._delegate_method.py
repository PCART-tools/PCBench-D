    def _delegate_method(self, name, *args, **kwargs):
        raise TypeError(f"You cannot call method {name}")
