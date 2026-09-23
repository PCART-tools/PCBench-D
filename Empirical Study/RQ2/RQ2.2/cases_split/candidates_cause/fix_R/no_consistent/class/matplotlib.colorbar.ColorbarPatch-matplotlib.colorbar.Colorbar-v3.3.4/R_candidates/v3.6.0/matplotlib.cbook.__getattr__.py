@_api.caching_module_getattr
class __getattr__:
    # module-level deprecations
    MatplotlibDeprecationWarning = _api.deprecated(
        "3.6", obj_type="",
        alternative="matplotlib.MatplotlibDeprecationWarning")(
        property(lambda self: _api.deprecation.MatplotlibDeprecationWarning))
    mplDeprecation = _api.deprecated(
        "3.6", obj_type="",
        alternative="matplotlib.MatplotlibDeprecationWarning")(
        property(lambda self: _api.deprecation.MatplotlibDeprecationWarning))
