def fort_subroutine_wrapper(name, ret_type, args):
    if name[0] in ['c', 's'] or name in ['zladiv', 'zdotu', 'zdotc']:
        wrapper = 'w' + name
    else:
        wrapper = name
    types, names = arg_names_and_types(args)
    argnames = ', '.join(names)

    names = [process_fortran_name(n, name) for n in names]
    argdecls = '\n        '.join('{0} {1}'.format(fortran_types[t], n)
                                 for n, t in zip(names, types))
    return fortran_template.format(name=name, wrapper=wrapper,
                                   argnames=argnames, argdecls=argdecls,
                                   ret_type=fortran_types[ret_type])
