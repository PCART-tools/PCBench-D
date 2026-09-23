def _deprecate_case_insensitive_join_cap(s):
    s_low = s.lower()
    if s != s_low:
        if s_low in ['miter', 'round', 'bevel']:
            cbook.warn_deprecated(
                "3.3", message="Case-insensitive capstyles are deprecated "
                "since %(since)s and support for them will be removed "
                "%(removal)s; please pass them in lowercase.")
        elif s_low in ['butt', 'round', 'projecting']:
            cbook.warn_deprecated(
                "3.3", message="Case-insensitive joinstyles are deprecated "
                "since %(since)s and support for them will be removed "
                "%(removal)s; please pass them in lowercase.")
        # Else, error out at the check_in_list stage.
    return s_low
