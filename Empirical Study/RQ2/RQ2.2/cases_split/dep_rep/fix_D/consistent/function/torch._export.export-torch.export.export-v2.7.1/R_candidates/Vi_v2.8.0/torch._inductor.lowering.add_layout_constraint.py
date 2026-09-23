def add_layout_constraint(fn, constraint):
    if isinstance(fn, torch._ops.OpOverloadPacket):
        for overload in fn.overloads():
            _maybe_layout_constraints[getattr(fn, overload)] = constraint
    else:
        _maybe_layout_constraints[fn] = constraint
