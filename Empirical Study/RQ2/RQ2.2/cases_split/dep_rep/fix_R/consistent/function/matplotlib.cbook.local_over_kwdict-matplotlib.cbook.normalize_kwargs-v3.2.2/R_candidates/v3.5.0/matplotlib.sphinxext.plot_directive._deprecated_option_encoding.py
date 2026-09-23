def _deprecated_option_encoding(arg):
    _api.warn_deprecated("3.5", name="encoding", obj_type="option")
    return directives.encoding(arg)
