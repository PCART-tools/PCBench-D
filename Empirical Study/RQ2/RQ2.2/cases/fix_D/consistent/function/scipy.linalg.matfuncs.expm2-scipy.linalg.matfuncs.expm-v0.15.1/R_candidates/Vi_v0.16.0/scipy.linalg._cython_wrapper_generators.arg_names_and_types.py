def arg_names_and_types(args):
    return zip(*[arg.split(' *') for arg in args.split(', ')])
