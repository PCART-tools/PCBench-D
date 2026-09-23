@register_op_strategy(
    [
        aten.split.Tensor,
        aten.split_with_sizes.default,
        aten.split_with_sizes_copy.default,
    ],
    RuntimeSchemaInfo(1),
)
def split_strategy(op_schema: OpSchema) -> TupleStrategy:
    input_strategy = op_schema.args_schema[0]
    split_size_or_sections = op_schema.args_schema[1]
    assert isinstance(input_strategy, OpStrategy)
    input_ndim = input_strategy.ndim
    split_dim = (
        cast(int, op_schema.args_schema[2]) if len(op_schema.args_schema) > 2 else 0
    )
    dim = normalize_dim(split_dim, input_ndim)

    # tensor to split cannot have Partial for now
    for arg_strategy in input_strategy.strategies:
        arg_spec = arg_strategy.output_spec
        if is_tensor_partial(arg_spec):
            raise NotImplementedError(
                f"splitting distributed tensor with "
                f"Partial placement is not implemented!\n"
                f"DTensorSpec={arg_strategy}"
            )

    def size_split(N, i) -> list:
        # Last chunk will be smaller if the tensor size N
        # along the given dimension dim is not divisible by i.
        assert i > 0
        return [i] * (N // i) + ([N % i] if N % i != 0 else [])

    output_size_list = (
        size_split(input_strategy.shape[dim], split_size_or_sections)
        if isinstance(split_size_or_sections, int)
        else split_size_or_sections
    )
    assert isinstance(output_size_list, Sized)

    split_strategies = []

    for _ in range(len(output_size_list)):
        op_strategy = OpStrategy([])

        for strategy in input_strategy.strategies:
            spec = strategy.output_spec
            placements = spec.placements
            if is_tensor_dim_sharded(spec, dim=dim):
                # if the input is sharded on the split dim, we need to unshard it
                placements = unshard_tensor_dim(spec.placements, dim=dim)

            spec = DTensorSpec(spec.mesh, placements)

            op_strategy.strategies.append(
                OpSpec(output_specs=spec, input_specs=([spec]))
            )
        split_strategies.append(op_strategy)

    return TupleStrategy(split_strategies)
