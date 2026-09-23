def get_all_kernel_argdefs(kernels):
    """
    The logic here must match with `get_all_call_args`, except no need to get arg_types here
    """
    argdefs_list = [get_kernel_argdefs(kernel) for kernel in kernels]

    return _get_all_args(argdefs_list)[0]
