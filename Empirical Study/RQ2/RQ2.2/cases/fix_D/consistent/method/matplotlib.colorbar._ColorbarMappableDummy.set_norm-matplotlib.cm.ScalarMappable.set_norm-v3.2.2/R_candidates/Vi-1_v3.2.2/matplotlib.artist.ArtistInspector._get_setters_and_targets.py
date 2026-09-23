    def _get_setters_and_targets(self):
        """
        Get the attribute strings and a full path to where the setter
        is defined for all setters in an object.
        """
        setters = []
        for name in dir(self.o):
            if not name.startswith('set_'):
                continue
            func = getattr(self.o, name)
            if (not callable(func)
                    or len(inspect.signature(func).parameters) < 2
                    or self.is_alias(func)):
                continue
            setters.append(
                (name[4:], f"{func.__module__}.{func.__qualname__}"))
        return setters
