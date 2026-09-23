def _maybe_cast_reduce_op_input(g, self):
    dtype = self.type().scalarType()
    # This check only covers traced modules where dtype is present
    if dtype is not None:
        # pytorch reduce-ops cast all other integral types to int64
        if not sym_help._is_fp(self) and not (dtype == "Long"):
            self = _cast_Long(g, self, False)  # type: ignore[name-defined]
    return self
