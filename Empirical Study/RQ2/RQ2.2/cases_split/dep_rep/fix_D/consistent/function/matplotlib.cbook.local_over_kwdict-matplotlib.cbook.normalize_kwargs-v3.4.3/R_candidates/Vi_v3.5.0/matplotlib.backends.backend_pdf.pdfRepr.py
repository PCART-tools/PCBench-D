def pdfRepr(obj):
    """Map Python objects to PDF syntax."""

    # Some objects defined later have their own pdfRepr method.
    if hasattr(obj, 'pdfRepr'):
        return obj.pdfRepr()

    # Floats. PDF does not have exponential notation (1.0e-10) so we
    # need to use %f with some precision.  Perhaps the precision
    # should adapt to the magnitude of the number?
    elif isinstance(obj, (float, np.floating)):
        if not np.isfinite(obj):
            raise ValueError("Can only output finite numbers in PDF")
        r = b"%.10f" % obj
        return r.rstrip(b'0').rstrip(b'.')

    # Booleans. Needs to be tested before integers since
    # isinstance(True, int) is true.
    elif isinstance(obj, bool):
        return [b'false', b'true'][obj]

    # Integers are written as such.
    elif isinstance(obj, (int, np.integer)):
        return b"%d" % obj

    # Unicode strings are encoded in UTF-16BE with byte-order mark.
    elif isinstance(obj, str):
        try:
            # But maybe it's really ASCII?
            s = obj.encode('ASCII')
            return pdfRepr(s)
        except UnicodeEncodeError:
            s = codecs.BOM_UTF16_BE + obj.encode('UTF-16BE')
            return pdfRepr(s)

    # Strings are written in parentheses, with backslashes and parens
    # escaped. Actually balanced parens are allowed, but it is
    # simpler to escape them all. TODO: cut long strings into lines;
    # I believe there is some maximum line length in PDF.
    elif isinstance(obj, bytes):
        return b'(' + _string_escape_regex.sub(_string_escape, obj) + b')'

    # Dictionaries. The keys must be PDF names, so if we find strings
    # there, we make Name objects from them. The values may be
    # anything, so the caller must ensure that PDF names are
    # represented as Name objects.
    elif isinstance(obj, dict):
        return fill([
            b"<<",
            *[Name(key).pdfRepr() + b" " + pdfRepr(obj[key])
              for key in sorted(obj)],
            b">>",
        ])

    # Lists.
    elif isinstance(obj, (list, tuple)):
        return fill([b"[", *[pdfRepr(val) for val in obj], b"]"])

    # The null keyword.
    elif obj is None:
        return b'null'

    # A date.
    elif isinstance(obj, datetime):
        return pdfRepr(_datetime_to_pdf(obj))

    # A bounding box
    elif isinstance(obj, BboxBase):
        return fill([pdfRepr(val) for val in obj.bounds])

    else:
        raise TypeError("Don't know a PDF representation for {} objects"
                        .format(type(obj)))
