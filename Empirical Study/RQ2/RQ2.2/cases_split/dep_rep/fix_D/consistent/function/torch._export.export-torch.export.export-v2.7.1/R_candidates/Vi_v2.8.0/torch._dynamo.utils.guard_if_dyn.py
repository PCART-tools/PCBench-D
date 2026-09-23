def guard_if_dyn(arg):
    from .variables import ConstantVariable

    arg = specialize_symnode(arg)

    if isinstance(arg, ConstantVariable):
        return arg.as_python_constant()

    return arg
