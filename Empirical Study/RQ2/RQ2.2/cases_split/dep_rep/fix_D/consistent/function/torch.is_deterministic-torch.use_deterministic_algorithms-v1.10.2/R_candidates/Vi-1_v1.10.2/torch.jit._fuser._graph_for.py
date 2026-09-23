def _graph_for(self, *args, **kwargs):
    try:
        dbs = self.get_debug_state()
        eps = list(dbs.execution_plans.values())
        assert(len(eps) == 1)
        graph = eps[0].graph.copy()

        # graph_executor_states for differentiable node
        fw_states = eps[0].code.differentiable_op_executor_states()
        diff_nodes: List[torch._C.Node] = []
        for n in graph.nodes():
            _get_differentiable_graph_node(n, diff_nodes)

        assert(len(fw_states) == len(diff_nodes))
        # swap each differentiable graph with optimized graph in their execution plan
        for n, state in zip(diff_nodes, fw_states):
            fw_execution_plans = list(state.execution_plans.values())
            assert(len(fw_execution_plans) == 1)
            n.g_('Subgraph', fw_execution_plans[0].graph)

        return graph
    except Exception:
        # fallback approach, we just ran the graph and return the recorded optimized
        # graph
        self(*args, **kwargs)
        return last_executed_optimized_graph()
