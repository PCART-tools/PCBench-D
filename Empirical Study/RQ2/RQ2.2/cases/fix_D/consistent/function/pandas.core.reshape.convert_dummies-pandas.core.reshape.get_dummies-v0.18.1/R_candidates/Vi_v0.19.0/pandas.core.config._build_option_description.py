def _build_option_description(k):
    """ Builds a formatted description of a registered option and prints it """

    o = _get_registered_option(k)
    d = _get_deprecated_option(k)

    s = u('%s ') % k

    if o.doc:
        s += '\n'.join(o.doc.strip().split('\n'))
    else:
        s += 'No description available.'

    if o:
        s += u('\n    [default: %s] [currently: %s]') % (o.defval,
                                                         _get_option(k, True))

    if d:
        s += u('\n    (Deprecated')
        s += (u(', use `%s` instead.') % d.rkey if d.rkey else '')
        s += u(')')

    s += '\n\n'
    return s
