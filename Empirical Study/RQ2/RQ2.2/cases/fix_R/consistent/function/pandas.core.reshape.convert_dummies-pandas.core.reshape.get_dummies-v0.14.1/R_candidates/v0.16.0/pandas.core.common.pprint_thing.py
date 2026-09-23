def pprint_thing(thing, _nest_lvl=0, escape_chars=None, default_escapes=False,
                 quote_strings=False):
    """
    This function is the sanctioned way of converting objects
    to a unicode representation.

    properly handles nested sequences containing unicode strings
    (unicode(object) does not)

    Parameters
    ----------
    thing : anything to be formatted
    _nest_lvl : internal use only. pprint_thing() is mutually-recursive
        with pprint_sequence, this argument is used to keep track of the
        current nesting level, and limit it.
    escape_chars : list or dict, optional
        Characters to escape. If a dict is passed the values are the
        replacements
    default_escapes : bool, default False
        Whether the input escape characters replaces or adds to the defaults

    Returns
    -------
    result - unicode object on py2, str on py3. Always Unicode.

    """
    def as_escaped_unicode(thing, escape_chars=escape_chars):
        # Unicode is fine, else we try to decode using utf-8 and 'replace'
        # if that's not it either, we have no way of knowing and the user
        # should deal with it himself.

        try:
            result = compat.text_type(thing)  # we should try this first
        except UnicodeDecodeError:
            # either utf-8 or we replace errors
            result = str(thing).decode('utf-8', "replace")

        translate = {'\t': r'\t',
                     '\n': r'\n',
                     '\r': r'\r',
                     }
        if isinstance(escape_chars, dict):
            if default_escapes:
                translate.update(escape_chars)
            else:
                translate = escape_chars
            escape_chars = list(escape_chars.keys())
        else:
            escape_chars = escape_chars or tuple()
        for c in escape_chars:
            result = result.replace(c, translate[c])

        return compat.text_type(result)

    if (compat.PY3 and hasattr(thing, '__next__')) or hasattr(thing, 'next'):
        return compat.text_type(thing)
    elif (isinstance(thing, dict) and
          _nest_lvl < get_option("display.pprint_nest_depth")):
        result = _pprint_dict(thing, _nest_lvl, quote_strings=True)
    elif is_sequence(thing) and _nest_lvl < \
            get_option("display.pprint_nest_depth"):
        result = _pprint_seq(thing, _nest_lvl, escape_chars=escape_chars,
                             quote_strings=quote_strings)
    elif isinstance(thing, compat.string_types) and quote_strings:
        if compat.PY3:
            fmt = "'%s'"
        else:
            fmt = "u'%s'"
        result = fmt % as_escaped_unicode(thing)
    else:
        result = as_escaped_unicode(thing)

    return compat.text_type(result)  # always unicode
