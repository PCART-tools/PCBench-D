    def remove_callback(self, func, *args, **kwargs):
        """
        Remove *func* from list of callbacks.

        *args* and *kwargs* are optional and used to distinguish between copies
        of the same function registered to be called with different arguments.
        This behavior is deprecated.  In the future, ``*args, **kwargs`` won't
        be considered anymore; to keep a specific callback removable by itself,
        pass it to `add_callback` as a `functools.partial` object.
        """
        if args or kwargs:
            _api.warn_deprecated(
                "3.1", message="In a future version, Timer.remove_callback "
                "will not take *args, **kwargs anymore, but remove all "
                "callbacks where the callable matches; to keep a specific "
                "callback removable by itself, pass it to add_callback as a "
                "functools.partial object.")
            self.callbacks.remove((func, args, kwargs))
        else:
            funcs = [c[0] for c in self.callbacks]
            if func in funcs:
                self.callbacks.pop(funcs.index(func))
