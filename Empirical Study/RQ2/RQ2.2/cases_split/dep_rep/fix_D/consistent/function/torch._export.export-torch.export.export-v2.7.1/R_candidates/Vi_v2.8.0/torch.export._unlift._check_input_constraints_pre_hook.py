@torch._dynamo.disable
def _check_input_constraints_pre_hook(self, args, kwargs):
    if not self.validate_inputs:
        return

    flat_args_with_path = _check_inputs_match(args, kwargs, self._in_spec)

    _check_input_constraints_for_graph(
        [node for node in self.graph.nodes if node.op == "placeholder"],
        flat_args_with_path,
        self.range_constraints,
    )
