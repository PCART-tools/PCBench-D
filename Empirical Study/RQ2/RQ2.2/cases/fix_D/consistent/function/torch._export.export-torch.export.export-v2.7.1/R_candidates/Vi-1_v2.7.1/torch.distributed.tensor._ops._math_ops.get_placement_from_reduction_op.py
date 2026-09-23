def get_placement_from_reduction_op(reduction_op: ReductionOpType) -> Placement:
    if isinstance(reduction_op, NormReduction):
        return _NormPartial(norm_type=reduction_op.norm_type)
    return Partial(reduction_op)
