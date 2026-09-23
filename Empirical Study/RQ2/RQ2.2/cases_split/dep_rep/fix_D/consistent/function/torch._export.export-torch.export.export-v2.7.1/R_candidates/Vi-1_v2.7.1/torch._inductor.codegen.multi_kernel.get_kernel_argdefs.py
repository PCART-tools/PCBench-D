def get_kernel_argdefs(kernel):
    arg_defs, _, _, _ = kernel.args.python_argdefs()
    return [x.name for x in arg_defs]
