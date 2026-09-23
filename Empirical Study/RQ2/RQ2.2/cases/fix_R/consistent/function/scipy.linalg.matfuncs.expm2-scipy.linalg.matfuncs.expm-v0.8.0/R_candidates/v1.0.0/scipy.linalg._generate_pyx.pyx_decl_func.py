def pyx_decl_func(name, ret_type, args, header_name):
    argtypes, argnames = arg_names_and_types(args)
    # Fix the case where one of the arguments has the same name as the
    # abbreviation for the argument type.
    # Otherwise the variable passed as an argument is considered overwrites
    # the previous typedef and Cython compilation fails.
    if ret_type in argnames:
        argnames = [n if n != ret_type else ret_type + '_' for n in argnames]
        argnames = [n if n not in ['lambda', 'in'] else n + '_'
                    for n in argnames]
        args = ', '.join([' *'.join([n, t])
                          for n, t in zip(argtypes, argnames)])
    argtypes = [npy_types.get(t, t) for t in argtypes]
    fort_args = ', '.join([' *'.join([n, t])
                           for n, t in zip(argtypes, argnames)])
    argnames = [arg_casts(t) + n for n, t in zip(argnames, argtypes)]
    argnames = ', '.join(argnames)
    c_ret_type = c_types[ret_type]
    args = args.replace('lambda', 'lambda_')
    return pyx_func_template.format(name=name, upname=name.upper(), args=args,
                                    fort_args=fort_args, ret_type=ret_type,
                                    c_ret_type=c_ret_type, argnames=argnames,
                                    header_name=header_name)
