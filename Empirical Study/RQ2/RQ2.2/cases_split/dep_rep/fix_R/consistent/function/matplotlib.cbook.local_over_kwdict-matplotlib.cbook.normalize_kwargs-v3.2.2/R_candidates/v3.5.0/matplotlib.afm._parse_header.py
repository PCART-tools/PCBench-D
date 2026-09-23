def _parse_header(fh):
    """
    Read the font metrics header (up to the char metrics) and returns
    a dictionary mapping *key* to *val*.  *val* will be converted to the
    appropriate python type as necessary; e.g.:

        * 'False'->False
        * '0'->0
        * '-168 -218 1000 898'-> [-168, -218, 1000, 898]

    Dictionary keys are

      StartFontMetrics, FontName, FullName, FamilyName, Weight,
      ItalicAngle, IsFixedPitch, FontBBox, UnderlinePosition,
      UnderlineThickness, Version, Notice, EncodingScheme, CapHeight,
      XHeight, Ascender, Descender, StartCharMetrics
    """
    header_converters = {
        b'StartFontMetrics': _to_float,
        b'FontName': _to_str,
        b'FullName': _to_str,
        b'FamilyName': _to_str,
        b'Weight': _to_str,
        b'ItalicAngle': _to_float,
        b'IsFixedPitch': _to_bool,
        b'FontBBox': _to_list_of_ints,
        b'UnderlinePosition': _to_float,
        b'UnderlineThickness': _to_float,
        b'Version': _to_str,
        # Some AFM files have non-ASCII characters (which are not allowed by
        # the spec).  Given that there is actually no public API to even access
        # this field, just return it as straight bytes.
        b'Notice': lambda x: x,
        b'EncodingScheme': _to_str,
        b'CapHeight': _to_float,  # Is the second version a mistake, or
        b'Capheight': _to_float,  # do some AFM files contain 'Capheight'? -JKS
        b'XHeight': _to_float,
        b'Ascender': _to_float,
        b'Descender': _to_float,
        b'StdHW': _to_float,
        b'StdVW': _to_float,
        b'StartCharMetrics': _to_int,
        b'CharacterSet': _to_str,
        b'Characters': _to_int,
    }
    d = {}
    first_line = True
    for line in fh:
        line = line.rstrip()
        if line.startswith(b'Comment'):
            continue
        lst = line.split(b' ', 1)
        key = lst[0]
        if first_line:
            # AFM spec, Section 4: The StartFontMetrics keyword
            # [followed by a version number] must be the first line in
            # the file, and the EndFontMetrics keyword must be the
            # last non-empty line in the file.  We just check the
            # first header entry.
            if key != b'StartFontMetrics':
                raise RuntimeError('Not an AFM file')
            first_line = False
        if len(lst) == 2:
            val = lst[1]
        else:
            val = b''
        try:
            converter = header_converters[key]
        except KeyError:
            _log.error('Found an unknown keyword in AFM header (was %r)' % key)
            continue
        try:
            d[key] = converter(val)
        except ValueError:
            _log.error('Value error parsing header in AFM: %s, %s', key, val)
            continue
        if key == b'StartCharMetrics':
            break
    else:
        raise RuntimeError('Bad parse')
    return d
