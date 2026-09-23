def constrain_to_fake_tensors(args, kwargs, fake_args, fake_kwargs):
    def apply_constraint(arg, fake_arg):
        if isinstance(arg, ir.IRNode):
            meta_stride_expr = [
                s.node.expr if isinstance(s, torch.SymInt) else s
                for s in fake_arg.stride()
            ]
            return ir.ExternKernel.require_exact_strides(arg, meta_stride_expr)
        if isinstance(arg, dict):
            return {
                key: apply_constraint(arg[key], fake_arg[key]) for key in arg.keys()
            }
        elif isinstance(arg, (tuple, list)):
            return type(arg)(
                apply_constraint(a, f_a) for (a, f_a) in zip(arg, fake_arg)
            )
        return arg

    args = tuple(
        apply_constraint(arg, fake_arg) for arg, fake_arg in zip(args, fake_args)
    )
    kwargs = {k: apply_constraint(v, fake_kwargs[k]) for k, v in kwargs.items()}
    return args, kwargs
