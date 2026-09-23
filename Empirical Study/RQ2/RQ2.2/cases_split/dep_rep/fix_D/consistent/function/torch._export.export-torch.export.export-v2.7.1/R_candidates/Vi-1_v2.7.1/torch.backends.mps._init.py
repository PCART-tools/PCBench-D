def _init():
    r"""Register prims as implementation of var_mean and group_norm."""
    global _lib

    if _lib is not None or not is_built():
        return

    from torch._decomp.decompositions import native_group_norm_backward
    from torch._refs import native_group_norm

    _lib = _Library("aten", "IMPL")  # noqa: TOR901
    _lib.impl("native_group_norm", native_group_norm, "MPS")
    _lib.impl("native_group_norm_backward", native_group_norm_backward, "MPS")
