def parse_compressed_namedshape(string):
    # This is a metalanguage for describing a shape of a tensor compactly.
    # 'N:3,C:2' -> size = [3, 2], names: ['N', 'C']
    # 'None:3,None:2' -> size = [3, 2], names: ['None', 'None']
    # '3,2' -> size = [3, 2], names=None passed to ctor.
    def parse_name(maybe_name):
        maybe_name = maybe_name.strip()
        if maybe_name == 'None':
            return None
        return maybe_name

    string = string.strip()

    # '' -> size: [], names:None
    if len(string) == 0:
        return None, []

    # '3, 2' -> size = [3, 2], None names.
    if ':' not in string:
        return None, [int(size) for size in string.split(',')]

    dims = string.split(',')
    tuples = [dim.split(':') for dim in dims]
    return zip(*[(parse_name(name), int(size)) for name, size in tuples])
