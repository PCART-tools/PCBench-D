@register_op_strategy(
    [
        aten._linalg_svd.default,
        aten.linalg_qr.default,
        # TODO: The diagonal ops can have an improved sharding strategy for
        # shard placements that does not require redistributing to replicate.
        aten.diagonal_copy.default,
        aten.diag_embed.default,
        aten.diag.default,
        aten.diagonal.default,
        aten.tril.default,
        aten.triu.default,
        aten._linalg_eigh.default,
        aten.upsample_bicubic2d.default,
        aten.upsample_bilinear2d.default,
        aten.upsample_linear1d.default,
        aten.upsample_nearest2d.default,
        aten.upsample_trilinear3d.default,
        # TODO: support the full F.interpolate set of options.
    ],
    schema_info=RuntimeSchemaInfo(1),
)
def linalg_replicate_strategy(op_schema: OpSchema) -> OpStrategy:
    """
    Since we do not have a simple way to compute some linear algebra operations
    like SVD or QR decomposition, always fall back to replicate.
    """
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    assert isinstance(input_strategy, OpStrategy), f"{input_strategy}"
    mesh = input_strategy.mesh

    output_strategies: list[OpSpec] = []
    for placement_strategy in input_strategy.strategies:
        replicate_placements = tuple(Replicate() for _ in range(mesh.ndim))
        replicate_spec = DTensorSpec(
            mesh=mesh,
            placements=replicate_placements,
            tensor_meta=placement_strategy.output_spec.tensor_meta,
        )
        redistribute_cost = [
            generate_redistribute_costs(input_strategy, replicate_spec)
        ]
        replicate_strategy = OpSpec(
            output_specs=replicate_spec,
            input_specs=(replicate_spec,),
            redistribute_cost=redistribute_cost,
        )
        output_strategies.append(replicate_strategy)
    return OpStrategy(output_strategies)
