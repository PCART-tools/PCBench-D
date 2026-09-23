@register_op_strategy(aten._scaled_mm.default)
def scaled_mm_strategy(op_schema: OpSchema) -> OpStrategy:
    mesh = op_schema.get_mesh_from_args()
    return _scaled_mm_like_strategy("mk,kn->mn", mesh, op_schema)
