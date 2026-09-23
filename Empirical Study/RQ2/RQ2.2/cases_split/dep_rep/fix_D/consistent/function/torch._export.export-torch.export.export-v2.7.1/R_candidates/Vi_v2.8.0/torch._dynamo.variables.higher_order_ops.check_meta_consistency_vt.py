def check_meta_consistency_vt(
    vars1: list[VariableTracker],
    vars2: list[VariableTracker],
    lhs_name: str,
    rhs_name: str,
    include_contiguity: bool = True,
) -> None:
    from torch._higher_order_ops.utils import check_meta_consistency

    from . import TensorVariable

    def _unwrap_var(var):
        if isinstance(var, TensorVariable):
            return var.proxy.node.meta["example_value"]
        elif isinstance(var, SymNodeVariable):
            return var.sym_num
        elif isinstance(var, ConstantVariable):
            return var.as_python_constant()
        else:
            unimplemented(f"Cannot unwrap var {var}")

    unwrapped1 = [_unwrap_var(var) for var in vars1]
    unwrapped2 = [_unwrap_var(var) for var in vars2]

    return check_meta_consistency(
        unwrapped1,
        unwrapped2,
        lhs_name,
        rhs_name,
        include_contiguity=include_contiguity,
    )
