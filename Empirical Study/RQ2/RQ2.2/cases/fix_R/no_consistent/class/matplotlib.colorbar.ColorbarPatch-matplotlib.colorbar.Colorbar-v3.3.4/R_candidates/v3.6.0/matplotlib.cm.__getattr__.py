@_api.caching_module_getattr  # module-level deprecations
class __getattr__:
    LUTSIZE = _api.deprecated(
        "3.5", obj_type="", alternative="rcParams['image.lut']")(
            property(lambda self: _LUTSIZE))
