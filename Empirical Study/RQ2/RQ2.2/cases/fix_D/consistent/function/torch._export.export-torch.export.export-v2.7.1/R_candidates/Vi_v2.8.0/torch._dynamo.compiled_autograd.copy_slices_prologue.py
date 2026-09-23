def copy_slices_prologue(
    inputs,
    base_sizes,
    base_strides,
    base_storage_offset,
    view_sizes,
    view_strides,
    view_storage_offset,
):
    grad = inputs[0]
    result = grad.new_empty_strided(base_sizes, base_strides)
    assert grad is not None
    result.copy_(grad)
    offset = view_storage_offset - base_storage_offset
    grad_slice = result.as_strided(view_sizes, view_strides, offset)
    return [result, grad_slice, grad_slice.clone(memory_format=torch.contiguous_format)]
