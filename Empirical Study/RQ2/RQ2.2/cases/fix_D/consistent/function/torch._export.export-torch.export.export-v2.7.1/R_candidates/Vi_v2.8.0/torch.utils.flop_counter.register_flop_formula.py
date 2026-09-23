def register_flop_formula(targets, get_raw=False) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def register_fun(flop_formula: Callable[_P, _T]) -> Callable[_P, _T]:
        if not get_raw:
            flop_formula = shape_wrapper(flop_formula)

        def register(target):
            if not isinstance(target, torch._ops.OpOverloadPacket):
                raise ValueError(
                    f"register_flop_formula(targets): expected each target to be "
                    f"OpOverloadPacket (i.e. torch.ops.mylib.foo), got "
                    f"{target} which is of type {type(target)}")
            if target in flop_registry:
                raise RuntimeError(f"duplicate registrations for {target}")
            flop_registry[target] = flop_formula

        # To handle allowing multiple aten_ops at once
        torch.utils._pytree.tree_map_(register, targets)

        return flop_formula

    return register_fun
