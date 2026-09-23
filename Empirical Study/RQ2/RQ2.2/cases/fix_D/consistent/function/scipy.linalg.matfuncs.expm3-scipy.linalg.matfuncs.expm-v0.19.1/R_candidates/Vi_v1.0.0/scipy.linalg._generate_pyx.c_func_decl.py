def c_func_decl(name, return_type, args):
    args = make_c_args(args)
    return_type = c_types[return_type]
    return c_func_template.format(name=name, upname=name.upper(),
                                  return_type=return_type, args=args)
