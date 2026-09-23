    def outer(t=t):

        def wrapper(*args, **kwargs):
            warnings.warn("pandas.core.common.{t} is deprecated. "
                          "These are not longer public API functions, "
                          "but can be imported from "
                          "pandas.types.common.{t} instead".format(t=t),
                          DeprecationWarning, stacklevel=3)
            return getattr(common, t)(*args, **kwargs)
        return wrapper
