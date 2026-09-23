@register_decomposition(aten.stack)
@out_wrapper()
def stack(tensors: TensorSequenceType, dim: int = 0) -> TensorLikeType:
    assert len(tensors) > 0, "stack expects a non-empty TensorList"
    wrapped_dim = utils.canonicalize_dim(tensors[0].ndim + 1, dim)
    # Refs need sparse support to check other condition
    if wrapped_dim < tensors[0].ndim:  # and not tensors[0].is_sparse:
        _check_stack_inputs(tensors)
        result_sizes = list(tensors[0].shape)
        result_sizes.insert(wrapped_dim, len(tensors))
        out = torch.cat(tensors, wrapped_dim)
        return out.view(result_sizes)

    # If dim == tensors[0].ndim, view cannot efficiently handle it
    return torch.cat([t.unsqueeze(wrapped_dim) for t in tensors], dim)
