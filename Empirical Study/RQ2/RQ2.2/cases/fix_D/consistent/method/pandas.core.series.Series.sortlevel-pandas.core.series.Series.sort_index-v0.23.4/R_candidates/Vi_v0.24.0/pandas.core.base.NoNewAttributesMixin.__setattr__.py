    def __setattr__(self, key, value):
        # _cache is used by a decorator
        # We need to check both 1.) cls.__dict__ and 2.) getattr(self, key)
        # because
        # 1.) getattr is false for attributes that raise errors
        # 2.) cls.__dict__ doesn't traverse into base classes
        if (getattr(self, "__frozen", False) and not
                (key == "_cache" or
                 key in type(self).__dict__ or
                 getattr(self, key, None) is not None)):
            raise AttributeError("You cannot add any new attribute '{key}'".
                                 format(key=key))
        object.__setattr__(self, key, value)
