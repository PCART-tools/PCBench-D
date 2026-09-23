@_api.caching_module_getattr  # module-level deprecations
class __getattr__:
    STYLE_FILE_PATTERN = _api.deprecated("3.5", obj_type="")(property(
        lambda self: re.compile(r'([\S]+).%s$' % STYLE_EXTENSION)))
