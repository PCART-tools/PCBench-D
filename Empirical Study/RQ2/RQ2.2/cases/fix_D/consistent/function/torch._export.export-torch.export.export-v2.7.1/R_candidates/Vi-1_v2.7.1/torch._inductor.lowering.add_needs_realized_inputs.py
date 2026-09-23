def add_needs_realized_inputs(fn):
    if isinstance(fn, (list, set, tuple, OrderedSet)):  # noqa: set_linter
        return [add_needs_realized_inputs(x) for x in fn]
    needs_realized_inputs.add(fn)
    if isinstance(fn, torch._ops.OpOverloadPacket):
        needs_realized_inputs.update(
            getattr(fn, overload) for overload in fn.overloads()
        )
