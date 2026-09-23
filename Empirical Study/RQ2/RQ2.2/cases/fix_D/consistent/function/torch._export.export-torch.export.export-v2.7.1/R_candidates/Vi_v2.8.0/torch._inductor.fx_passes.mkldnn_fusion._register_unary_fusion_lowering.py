    def _register_unary_fusion_lowering(
        pattern, unary_attr, computation_op, lowp_dtype=None
    ):
        @register_lowering_pattern(
            pattern,
            extra_check=_is_valid_computation_unary_fusion(computation_op, lowp_dtype),
        )
        def fn(match, *args, **kwargs):
            computation_args = list(args)[:-3] + [
                unary_attr.op_name,
                unary_attr.scalars_attr,
                unary_attr.algorithm_attr,
            ]
            counters["inductor"]["mkldnn_unary_fusion_matcher_count"] += 1
            counters["inductor"]["mkldnn_unary_fusion_matcher_nodes"] += len(
                match.nodes
            )
            return L[computation_op](*computation_args)

        return fn
