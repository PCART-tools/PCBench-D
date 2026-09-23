def _cat_meta(tensors: Sequence[TensorLikeType], dim: int) -> TensorLikeType:
    # Verifies same shape (except in the concat dimension)
    assert dim >= 0
    shape = tensors[0].shape
    sym_sum_args = []
    for tensor_idx, tensor in enumerate(tensors):
        assert len(shape) == len(tensor.shape)
        for idx, (common_length, length) in enumerate(zip(shape, tensor.shape)):
            if idx == dim:
                sym_sum_args.append(length)
            else:
                torch._check(
                    length == common_length,
                    lambda: f"Sizes of tensors must match except in dimension {dim}. "
                    f"Expected {common_length} in dimension {idx} but got {length} for tensor number "
                    f"{tensor_idx} in the list",
                )

    new_shape = list(tensors[0].shape).copy()
    new_shape[dim] = torch.sym_sum(sym_sum_args)
    return TensorMeta(
        tensors[0],
        shape=new_shape,
        strides=utils.make_contiguous_strides_for(new_shape),
    )
