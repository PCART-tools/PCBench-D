    def __init_subclass__(cls, **kwargs) -> None:
        factorize = getattr(cls, "factorize")
        if (
            "use_na_sentinel" not in inspect.signature(factorize).parameters
            # TimelikeOps uses old factorize args to ensure we don't break things
            and cls.__name__ not in ("TimelikeOps", "DatetimeArray", "TimedeltaArray")
        ):
            # See GH#46910 for details on the deprecation
            name = cls.__name__
            warnings.warn(
                f"The `na_sentinel` argument of `{name}.factorize` is deprecated. "
                f"In the future, pandas will use the `use_na_sentinel` argument "
                f"instead.  Add this argument to `{name}.factorize` to be compatible "
                f"with future versions of pandas and silence this warning.",
                DeprecationWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
