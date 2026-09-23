def c_sub_decl(name, return_type, args):
    args = make_c_args(args)
    return c_sub_template.format(name=name, upname=name.upper(), args=args)
