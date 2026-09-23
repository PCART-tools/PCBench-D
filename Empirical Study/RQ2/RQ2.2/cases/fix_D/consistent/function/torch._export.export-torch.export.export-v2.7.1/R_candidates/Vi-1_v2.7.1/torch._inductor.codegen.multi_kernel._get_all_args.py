def _get_all_args(args_list, arg_types_list=None):
    all_args = max(args_list, key=len)[:]
    arg_types = max(arg_types_list, key=len)[:] if arg_types_list is not None else None
    for args in args_list:
        assert OrderedSet(args).issubset(OrderedSet(all_args)), (
            f"{args} v.s. {all_args}"
        )

    return all_args, arg_types
