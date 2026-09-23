def make_c_args(args):
    types, names = arg_names_and_types(args)
    types = [c_types[arg] for arg in types]
    return ', '.join('{0} *{1}'.format(t, n) for t, n in zip(types, names))
