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
        # Manually copy the signature instead of using functools.wraps because
        # displaying the Axis method source when asking for the Axes method
        # source would be confusing.
        wrapped_method = getattr(maxis.Axis, self.method_name)
        wrapper.__signature__ = inspect.signature(wrapped_method)
        doc = wrapped_method.__doc__
        if doc:
            doc_sub = {"this Axis": f"the {self.attr_name}",
                       **(self.doc_sub or {})}
            for k, v in doc_sub.items():
                assert k in doc, \
                    (f"The definition of {wrapper.__qualname__} expected that "
                     f"the docstring of Axis.{self.method_name} contains "
                     f"{k!r} as a substring.")
                doc = doc.replace(k, v)
            wrapper.__doc__ = inspect.cleandoc(doc)

        setattr(owner, name, wrapper)
