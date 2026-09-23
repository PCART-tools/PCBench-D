def pxd_decl(name, ret_type, args):
    args = args.replace('lambda', 'lambda_').replace('*in,', '*in_,')
    return pxd_template.format(name=name, ret_type=ret_type, args=args)
