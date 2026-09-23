    def _register_binary_unary_fusion_lowering(
        pattern,
        computation_op,
        binary_op,
        fusion_op,
        unary_attr=None,
    ):
        @register_lowering_pattern(
            pattern, extra_check=_is_valid_computation_binary(computation_op, binary_op)
        )
        def fn(match, *args, **kwargs):
            other = kwargs.get("other")
            assert isinstance(other, ir.TensorBox)
            binary_attr = _binary_attr[binary_op]
            args_list = list(args)
            computation_args = [args_list[0], other] + args_list[1:-3] + [binary_attr]
            if len(args_list) > 6:
                if unary_attr is not None:
                    computation_args += [
                        1.0,
                        unary_attr.op_name,
                        unary_attr.scalars_attr,
                        unary_attr.algorithm_attr,
                    ]
                else:
                    computation_args += [1.0, None, [], None]
            counters["inductor"]["mkldnn_conv_binary_unary_fusion_matcher_count"] += 1
            counters["inductor"]["mkldnn_conv_binary_unary_fusion_matcher_nodes"] += (
                len(match.nodes)
            )
            return L[fusion_op](*computation_args)

        return fn
