def prim_tolist(g, input, dim_val, elem_ty_val):
    dim = sym_help._maybe_get_const(dim_val, "i")
    if dim > 1:
        return _unimplemented("prim_tolist", "dim_val > 1")
    return input
