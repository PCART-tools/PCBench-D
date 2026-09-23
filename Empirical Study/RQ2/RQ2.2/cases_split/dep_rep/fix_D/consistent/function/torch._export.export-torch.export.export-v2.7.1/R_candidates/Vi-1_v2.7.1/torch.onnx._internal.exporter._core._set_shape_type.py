def _set_shape_type(
    value: ir.Value,
    meta_val: torch.Tensor
    | torch.SymBool
    | torch.SymInt
    | torch.SymFloat
    | tuple[torch.Tensor],
    complex_to_float: bool,
) -> None:
    # TODO: Consider using meta["tensor_meta"] for this? Would it be faster?
    if isinstance(meta_val, tuple):
        logger.warning("Setting shape and type of tensors is not supported yet")
    if isinstance(meta_val, torch.Tensor):
        # FIXME: Consider shape for complex values
        dims = []
        for dim in meta_val.shape:
            if isinstance(dim, int):
                dims.append(dim)
            else:
                dims.append(str(dim.node))
        value.dtype = _torch_dtype_to_onnx_dtype(meta_val.dtype)
        if complex_to_float:
            if meta_val.dtype == torch.complex64:
                value.dtype = ir.DataType.FLOAT
                # Add 2 as the last dimension if the tensor is complex to hold the real/imag parts
                dims.append(2)
            elif meta_val.dtype == torch.complex128:
                value.dtype = ir.DataType.DOUBLE
                # Add 2 as the last dimension if the tensor is complex to hold the real/imag parts
                dims.append(2)

        value.shape = ir.Shape(dims)
    elif isinstance(meta_val, (int, torch.SymInt)):
        # aten::sym_size output is a int, not a tensor, which stands
        # for the size of one dim. We treat it as a scalar.
        value.dtype = ir.DataType.INT64
        value.shape = ir.Shape([])
    elif isinstance(meta_val, (bool, torch.SymBool)):
        value.dtype = ir.DataType.BOOL
        value.shape = ir.Shape([])
    elif isinstance(meta_val, (float, torch.SymFloat)):
        value.dtype = ir.DataType.FLOAT
        value.shape = ir.Shape([])
    else:
        pass
