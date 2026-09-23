    def __setattr__(self, key, value):
        # _cache is used by a decorator
        # dict lookup instead of getattr as getattr is false for getter
        # which error
        if getattr(self, "__frozen", False) and not \
                (key in type(self).__dict__ or key == "_cache"):
            raise AttributeError("You cannot add any new attribute '{key}'".
                                 format(key=key))
        object.__setattr__(self, key, value)
