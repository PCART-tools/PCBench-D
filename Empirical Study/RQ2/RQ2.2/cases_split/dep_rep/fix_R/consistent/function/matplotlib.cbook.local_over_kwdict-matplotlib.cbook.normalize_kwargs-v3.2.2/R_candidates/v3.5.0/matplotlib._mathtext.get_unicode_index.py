def get_unicode_index(symbol, math=True):
    r"""
    Return the integer index (from the Unicode table) of *symbol*.

    Parameters
    ----------
    symbol : str
        A single unicode character, a TeX command (e.g. r'\pi') or a Type1
        symbol name (e.g. 'phi').
    math : bool, default: True
        If False, always treat as a single unicode character.
    """
    # for a non-math symbol, simply return its unicode index
    if not math:
        return ord(symbol)
    # From UTF #25: U+2212 minus sign is the preferred
    # representation of the unary and binary minus sign rather than
    # the ASCII-derived U+002D hyphen-minus, because minus sign is
    # unambiguous and because it is rendered with a more desirable
    # length, usually longer than a hyphen.
    if symbol == '-':
        return 0x2212
    try:  # This will succeed if symbol is a single unicode char
        return ord(symbol)
    except TypeError:
        pass
    try:  # Is symbol a TeX symbol (i.e. \alpha)
        return tex2uni[symbol.strip("\\")]
    except KeyError as err:
        raise ValueError(
            "'{}' is not a valid Unicode character or TeX/Type1 symbol"
            .format(symbol)) from err
