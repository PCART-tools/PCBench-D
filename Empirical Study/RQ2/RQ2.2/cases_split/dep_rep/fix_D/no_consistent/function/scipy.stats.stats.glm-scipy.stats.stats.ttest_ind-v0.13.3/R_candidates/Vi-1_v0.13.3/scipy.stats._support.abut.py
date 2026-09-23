def abut(source, *args):
    # comment: except for the repetition, this is equivalent to hstack.
    """\nLike the |Stat abut command.  It concatenates two arrays column-wise
    and returns the result.  CAUTION:  If one array is shorter, it will be
    repeated until it is as long as the other.

    Format:  abut (source, args)    where args=any # of arrays
    Returns: an array as long as the LONGEST array past, source appearing on the
    'left', arrays in <args> attached on the 'right'.\n"""

    source = asarray(source)
    if len(source.shape) == 1:
        width = 1
        source = np.resize(source,[source.shape[0],width])
    else:
        width = source.shape[1]
    for addon in args:
        if len(addon.shape) == 1:
            width = 1
            addon = np.resize(addon,[source.shape[0],width])
        else:
            width = source.shape[1]
        if len(addon) < len(source):
            addon = np.resize(addon,[source.shape[0],addon.shape[1]])
        elif len(source) < len(addon):
            source = np.resize(source,[addon.shape[0],source.shape[1]])
        source = np.concatenate((source,addon),1)
    return source
