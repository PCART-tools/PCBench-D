    def _is_valid_grouped_gemm_fusion(computation_nodes):
        """
        Here we check:
        1. More than 1 GEMM nodes has been found.
        2. All the GEMM nodes share the same activation.
        3. All the GEMM nodes have same weight size but different wgt node.
        """
        computation_op = mkldnn._linear_pointwise.default
        act = computation_nodes[0].args[0]
        wgt = computation_nodes[0].args[1]
        wgt_size = wgt.meta.get("val").size()  # type: ignore[union-attr]
        return len(computation_nodes) >= 2 and all(
            (
                node.target == computation_op
                and node.args[0] == act
                and (node.args[1].meta.get("val").size() == wgt_size)
                and (node.args[1] != wgt or gemm_idx == 0)
            )
            for gemm_idx, node in enumerate(computation_nodes)
        )
