def warn_deprecated(api, new_api=None):
    warning = get_warning(api, new_api, replace_newlines=True)
    warnings.warn(warning, FutureWarning, stacklevel=3)
