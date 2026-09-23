def default_fused_keys_renamer(keys):
    """Create new keys for fused tasks"""
    typ = type(keys[0])
    if typ is str or typ is unicode:
        names = [key_split(x) for x in keys[:0:-1]]
        names.append(keys[0])
        return '-'.join(names)
    elif (typ is tuple and len(keys[0]) > 0 and
          isinstance(keys[0][0], (str, unicode))):
        names = [key_split(x) for x in keys[:0:-1]]
        names.append(keys[0][0])
        return ('-'.join(names),) + keys[0][1:]
    else:
        return None
