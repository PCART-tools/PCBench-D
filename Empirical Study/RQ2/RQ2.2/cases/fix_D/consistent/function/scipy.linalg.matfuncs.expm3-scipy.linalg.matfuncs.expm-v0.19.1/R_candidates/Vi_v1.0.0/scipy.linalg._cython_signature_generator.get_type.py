def get_type(info, arg):
    argtype = sig_types[info['vars'][arg]['typespec']]
    if argtype == 'c' and info['vars'][arg].get('kindselector') is not None:
        argtype = 'z'
    return argtype
