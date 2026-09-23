class _axis_method_wrapper:
    """
    Helper to generate Axes methods wrapping Axis methods.

    After ::

        get_foo = _axis_method_wrapper("xaxis", "get_bar")

    (in the body of a class) ``get_foo`` is a method that forwards it arguments
    to the ``get_bar`` method of the ``xaxis`` attribute, and gets its
    signature and docstring from ``Axis.get_bar``.

    The docstring of ``get_foo`` is built by replacing "this Axis" by "the
    {attr_name}" (i.e., "the xaxis", "the yaxis") in the wrapped method's
    dedented docstring; additional replacements can by given in *doc_sub*.
    """

    def __init__(self, attr_name, method_name, *, doc_sub=None):
        self.attr_name = attr_name
        self.method_name = method_name
        # Immediately put the docstring in ``self.__doc__`` so that docstring
        # manipulations within the class body work as expected.
        doc = inspect.getdoc(getattr(maxis.Axis, method_name))
        self._missing_subs = []
        if doc:
            doc_sub = {"this Axis": f"the {self.attr_name}", **(doc_sub or {})}
            for k, v in doc_sub.items():
                if k not in doc:  # Delay raising error until we know qualname.
                    self._missing_subs.append(k)
                doc = doc.replace(k, v)
        self.__doc__ = doc

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
