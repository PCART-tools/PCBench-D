@_api.caching_module_getattr
class __getattr__:
    NO_ESCAPE = _api.deprecated("3.6", obj_type="")(
        property(lambda self: _NO_ESCAPE))
    re_mathsep = _api.deprecated("3.6", obj_type="")(
        property(lambda self: _split_math.__self__))
