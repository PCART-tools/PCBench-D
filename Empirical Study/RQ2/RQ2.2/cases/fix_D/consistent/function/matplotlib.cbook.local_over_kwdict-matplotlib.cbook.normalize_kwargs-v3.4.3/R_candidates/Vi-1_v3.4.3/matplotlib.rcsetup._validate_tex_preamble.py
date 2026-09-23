def _validate_tex_preamble(s):
    if s is None or s == 'None':
        _api.warn_deprecated(
            "3.3", message="Support for setting the 'text.latex.preamble' or "
            "'pgf.preamble' rcParam to None is deprecated since %(since)s and "
            "will be removed %(removal)s; set it to an empty string instead.")
        return ""
    try:
        if isinstance(s, str):
            return s
        elif np.iterable(s):
            _api.warn_deprecated(
                "3.3", message="Support for setting the 'text.latex.preamble' "
                "or 'pgf.preamble' rcParam to a list of strings is deprecated "
                "since %(since)s and will be removed %(removal)s; set it to a "
                "single string instead.")
            return '\n'.join(s)
        else:
            raise TypeError
    except TypeError as e:
        raise ValueError('Could not convert "%s" to string' % s) from e
