@register_decomposition(aten.lerp)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("start", "end", "weight"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def lerp(start: Tensor, end: Tensor, weight: Union[Tensor, NumberType]):
    inputs = [start, end]
    if isinstance(weight, Number):
        weight = start.new_full((), weight)  # type: ignore[arg-type]
    else:
        inputs.append(weight)
    assert isinstance(weight, Tensor)  # mypy
    # We implement it this way for numerical stability. We assume (in the stability optimisation)
    # that 0 <= weight <= 1. We take the abs to deal with complex numbers
    # We want to perform operations near zero, which is where floating points are most precise
    # thus, we perform the following optimisation:
    # If weight.abs() >= 0.5:
    #    return (1 - weight) * (start - end) + end
    mask = weight.abs() >= 0.5
    coeff = torch.where(mask, weight - 1, weight)
    base = torch.where(mask, end, start)
    output = coeff * (end - start) + base
    # make sure the decomposition output's stride is same as non-decomposition path.
    stride = utils.compute_elementwise_output_strides(*_maybe_broadcast(*inputs))
    if output.stride() != stride:
        output = prims.copy_strided(output, stride)

    return handle_noncontiguous_outputs(inputs, output)
