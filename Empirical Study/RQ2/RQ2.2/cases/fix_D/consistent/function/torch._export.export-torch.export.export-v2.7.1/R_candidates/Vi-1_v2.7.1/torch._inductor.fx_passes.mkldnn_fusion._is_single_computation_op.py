    def _is_single_computation_op(computation_op, lowp_dtype=None):
        def fn(match):
            computation_nodes = filter_nodes(match.nodes, computation_op)

            if lowp_dtype:
                output_node_meta = match.output_node().meta.get("val")
                if output_node_meta.dtype != lowp_dtype:
                    return False

            if len(computation_nodes) < 1:
                return False
            if any(n.args[-3] != "none" for n in computation_nodes):
                return False
            return True

        return fn
