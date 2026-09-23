def record_automatic_dynamic(
    tx: "InstructionTranslator", name: str, e: torch.Tensor
) -> FrameStateSizeEntry:
    # This mimics stride inference algorithm in _create_symbolic_sizes_strides_storage_offset
    ex_size = e.size()
    if not is_sparse_any(e):
        ex_stride = e.stride()
        dim = e.dim()

        stride = [None] * dim
        pending = [(ex_stride[i], -i) for i in range(dim)]
        pending.sort(key=_nested_int_aware_sort)
        candidates = {}
        for i_stride, neg_i in pending:
            i = -neg_i
            stride[i] = candidates.get(i_stride, i_stride)
            candidates.setdefault(i_stride * ex_size[i], InferStride(i))
    else:
        stride = []

    return process_automatic_dynamic(
        tx, name, FrameStateSizeEntry.make_tensor(tuple(ex_size), tuple(stride))
    )
