def create_traced_fn(self, fn):
    def traced_fn(*inputs, **kwargs):
        fn_tensors, inputs_tensors = partial_apply_nontensors(fn, inputs, **kwargs)
        # `check_trace` is set to False because check_trace is run with @no_grad
        # Also, `check_against_reference` already does all the checks
        # against python function
        traced = torch.jit.trace(fn_tensors, inputs_tensors, check_trace=False)
        self.assertExportImport(traced.graph, inputs_tensors)
        output = traced(*inputs_tensors)
        # skip type annotate function attributes for now, see: https://github.com/python/mypy/issues/2087
        traced_fn.last_graph = traced.graph_for(*inputs_tensors)  # type: ignore[attr-defined]
        traced_fn.graph = traced.graph  # type: ignore[attr-defined]
        return output
    return traced_fn
