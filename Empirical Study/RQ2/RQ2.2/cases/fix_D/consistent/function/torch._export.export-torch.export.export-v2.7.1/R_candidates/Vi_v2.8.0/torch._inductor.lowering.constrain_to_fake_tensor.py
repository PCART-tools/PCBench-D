def constrain_to_fake_tensor(arg, fake_arg):
    if isinstance(arg, ir.IRNode):
        meta_stride_expr = [
            s.node.expr if isinstance(s, torch.SymInt) else s for s in fake_arg.stride()
        ]
        return ir.ExternKernel.require_exact_strides(arg, meta_stride_expr)
    if isinstance(arg, dict):
        return {
            key: constrain_to_fake_tensor(arg[key], fake_arg[key]) for key in arg.keys()
        }
    elif isinstance(arg, (tuple, list)):
        return type(arg)(
            constrain_to_fake_tensor(a, f_a) for (a, f_a) in zip(arg, fake_arg)
        )
    return arg
