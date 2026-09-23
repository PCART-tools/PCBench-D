@register_decomposition(aten.repeat)
@out_wrapper()
def repeat(a: Tensor, *repeat_shape) -> Tensor:
    repeat_shape = utils.extract_shape_from_varargs(repeat_shape, validate=False)
    torch._check(
        len(repeat_shape) >= len(a.shape),
        lambda: "repeat: Number of dimensions of repeat dims can not be smaller than number of dimensions of tensor",
    )

    if len(repeat_shape) == 0:
        return torch.clone(a)

    num_new_dimensions = len(repeat_shape) - a.ndim
    padded_shape = [1] * num_new_dimensions
    for dim_size in a.shape:
        padded_shape.append(dim_size)

    target_shape = tuple(
        padded_size * repeat_size
        for padded_size, repeat_size in zip(padded_shape, repeat_shape)
    )

    # return an empty tensor if one of the repeat_shape dimensions is zero
    if 0 in repeat_shape:
        return torch.empty(
            target_shape,
            dtype=a.dtype,
            device=a.device,
            requires_grad=a.requires_grad,
            memory_format=utils.suggest_memory_format(a),
        )

    urtensor_shape = target_shape
    urtensor_stride = utils.make_contiguous_strides_for(target_shape)
    for dim, dim_size in enumerate(padded_shape):
        # repeat each dimension by using unfold_copy operation
        urtensor_shape, urtensor_stride = _get_unfold_shape_stride(
            urtensor_shape, urtensor_stride, dim, dim_size, max(dim_size, 1)
        )

    # derive permute order by sorting urtensor strides
    enumerated_stride = list(enumerate(urtensor_stride))
    enumerated_stride.sort(key=operator.itemgetter(1), reverse=True)
    permute_order, _sorted_stride = zip(*enumerated_stride)

    # add new and expand dimensions according to urtensor
    repeat_xtensor = a.expand(urtensor_shape)

    # clone tensor to concretize expanded dimensions
    cloned_result = torch.clone(repeat_xtensor)

    # transpose axis so strides are in sorted order
    permuted_result = cloned_result.permute(permute_order)

    # reshape to get contiguous tensor with correct target shape
    return permuted_result.reshape(target_shape)
