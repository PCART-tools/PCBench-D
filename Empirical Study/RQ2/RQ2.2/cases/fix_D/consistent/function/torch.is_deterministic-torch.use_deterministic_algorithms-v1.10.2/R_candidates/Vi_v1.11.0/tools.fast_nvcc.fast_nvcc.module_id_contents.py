def module_id_contents(command: List[str]) -> str:
    """
    Guess the contents of the .module_id file contained within command.
    """
    if command[0] == 'cicc':
        path = command[-3]
    elif command[0] == 'cudafe++':
        path = command[-1]
    middle = pathlib.PurePath(path).name.replace('-', '_').replace('.', '_')
    # this suffix is very wrong (the real one is far less likely to be
    # unique), but it seems difficult to find a rule that reproduces the
    # real suffixes, so here's one that, while inaccurate, is at least
    # hopefully as straightforward as possible
    suffix = hashlib.md5(str.encode(middle)).hexdigest()[:8]
    return f'_{len(middle)}_{middle}_{suffix}'
