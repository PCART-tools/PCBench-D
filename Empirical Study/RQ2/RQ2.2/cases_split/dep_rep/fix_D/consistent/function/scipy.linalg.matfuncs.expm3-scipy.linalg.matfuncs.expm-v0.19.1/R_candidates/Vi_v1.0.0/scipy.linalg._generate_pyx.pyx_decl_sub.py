def pyx_decl_sub(name, args, header_name):
    argtypes, argnames = arg_names_and_types(args)
    argtypes = [npy_types.get(t, t) for t in argtypes]
    argnames = [n if n not in ['lambda', 'in'] else n + '_' for n in argnames]
    fort_args = ', '.join([' *'.join([n, t])
                           for n, t in zip(argtypes, argnames)])
    argnames = [arg_casts(t) + n for n, t in zip(argnames, argtypes)]
    argnames = ', '.join(argnames)
    args = args.replace('*lambda,', '*lambda_,').replace('*in,', '*in_,')
    return pyx_sub_template.format(name=name, upname=name.upper(),
                                   args=args, fort_args=fort_args,
                                   argnames=argnames, header_name=header_name)
