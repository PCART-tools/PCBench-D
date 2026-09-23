@register_op_strategy(aten.constant_pad_nd.default)
def constant_pad_nd_strategy(op_schema: OpSchema) -> OpStrategy:
    mesh = op_schema.get_mesh_from_args(validate=False)

    # TODO(d4l3k); implement a more correct strategy for constant_pad_nd
    return OpStrategy(
        [
            OpSpec(
                output_specs=DTensorSpec(mesh, (Replicate(),)),
                input_specs=(
                    DTensorSpec(mesh, (Replicate(),)),
                    DTensorSpec(mesh, (Replicate(),)),
                ),
                redistribute_cost=[[1]],
            )
        ]
    )
