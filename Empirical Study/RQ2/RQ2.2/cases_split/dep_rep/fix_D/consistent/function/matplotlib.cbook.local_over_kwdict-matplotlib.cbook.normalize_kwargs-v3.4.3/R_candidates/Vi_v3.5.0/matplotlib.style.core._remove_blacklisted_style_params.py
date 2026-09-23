def _remove_blacklisted_style_params(d, warn=True):
    o = {}
    for key in d:  # prevent triggering RcParams.__getitem__('backend')
        if key in STYLE_BLACKLIST:
            if warn:
                _api.warn_external(
                    f"Style includes a parameter, {key!r}, that is not "
                    "related to style.  Ignoring this parameter.")
        else:
            o[key] = d[key]
    return o
