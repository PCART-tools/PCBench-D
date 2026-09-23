def _slice(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    axes: list | torch.Tensor | torch._C.Value,
    starts: list | torch.Tensor | torch._C.Value,
    ends: list | torch.Tensor | torch._C.Value,
    steps: list | torch.Tensor | torch._C.Value | None = None,
):
    def is_none_value(value):
        if value is None:
            return True
        return (
            isinstance(value, torch._C.Value)
            and value.node().kind() == "prim::Constant"
            and isinstance(value.type(), _C.NoneType)
        )

    def to_slice_input(list_or_value, default_value=None):
        # Convert input param into a 1D torch.Value.
        if is_none_value(list_or_value) and default_value is not None:
            list_or_value = [default_value]

        if isinstance(list_or_value, (list, torch.Tensor)):
            return g.op("Constant", value_t=torch.tensor(list_or_value))

        rank = symbolic_helper._get_tensor_rank(list_or_value)
        if rank == 0:
            return symbolic_helper._unsqueeze_helper(g, list_or_value, [0])
        if rank == 1:
            return list_or_value
        raise errors.SymbolicValueError(
            f"Rank must be 0 or 1, not {rank}", list_or_value
        )

    def get_const_value(list_or_value):
        if isinstance(list_or_value, (list, torch.Tensor)):
            if len(list_or_value) == 1:
                return list_or_value[0]
            return None
        return symbolic_helper._maybe_get_const(list_or_value, "i")

    # Check if slice is a no-op
    if (
        get_const_value(starts) == 0
        and get_const_value(ends) == _constants.INT64_MAX
        and (steps is None or get_const_value(steps) == 1)
    ):
        return input

    axes = to_slice_input(axes)
    starts = to_slice_input(starts, default_value=0)
    ends = to_slice_input(ends, default_value=_constants.INT64_MAX)
    if steps is None:
        return g.op("Slice", input, starts, ends, axes)
    steps = to_slice_input(steps, default_value=1)
    return g.op("Slice", input, starts, ends, axes, steps)
