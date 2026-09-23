def make_signature(filename):
    info = crackfortran.crackfortran(filename)[0]
    name = info['name']
    if info['block'] == 'subroutine':
        return_type = 'void'
    else:
        return_type = get_type(info, name)
    arglist = [' *'.join([get_type(info, arg), arg]) for arg in info['args']]
    args = ', '.join(arglist)
    # Eliminate strange variable naming that replaces rank with rank_bn.
    args = args.replace('rank_bn', 'rank')
    return '{} {}({})\n'.format(return_type, name, args)
