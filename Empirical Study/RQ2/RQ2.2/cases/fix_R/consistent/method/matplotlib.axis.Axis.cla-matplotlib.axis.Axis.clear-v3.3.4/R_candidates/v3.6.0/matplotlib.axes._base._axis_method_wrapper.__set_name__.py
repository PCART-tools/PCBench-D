    def __set_name__(self, owner, name):
        # This is called at the end of the class body as
        # ``self.__set_name__(cls, name_under_which_self_is_assigned)``; we
        # rely on that to give the wrapper the correct __name__/__qualname__.
        get_method = attrgetter(f"{self.attr_name}.{self.method_name}")

        def wrapper(self, *args, **kwargs):
            return get_method(self)(*args, **kwargs)

        wrapper.__module__ = owner.__module__
        wrapper.__name__ = name
        wrapper.__qualname__ = f"{owner.__qualname__}.{name}"
        wrapper.__doc__ = self.__doc__
        # Manually copy the signature instead of using functools.wraps because
        # displaying the Axis method source when asking for the Axes method
        # source would be confusing.
        wrapper.__signature__ = inspect.signature(
            getattr(maxis.Axis, self.method_name))

        if self._missing_subs:
            raise ValueError(
                "The definition of {} expected that the docstring of Axis.{} "
                "contains {!r} as substrings".format(
                    wrapper.__qualname__, self.method_name,
                    ", ".join(map(repr, self._missing_subs))))

        setattr(owner, name, wrapper)
