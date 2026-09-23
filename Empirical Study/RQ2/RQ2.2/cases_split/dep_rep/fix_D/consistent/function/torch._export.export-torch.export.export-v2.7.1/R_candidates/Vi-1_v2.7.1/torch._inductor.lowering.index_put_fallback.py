def index_put_fallback(self, indices, values, accumulate):
    deterministic = torch.are_deterministic_algorithms_enabled()
    if is_triton(values) and (accumulate or deterministic):
        msg = (
            "index put with accumulate."
            if not deterministic
            else "deterministic index put."
        )
        if stack_trace := V.graph.current_node.meta.get("stack_trace", None):
            msg = f"{msg} Found from : \n {stack_trace}"
        V.graph.disable_cudagraphs_reason = msg

    ir.IndexPutFallback(V.graph.current_node.target, self, indices, values, accumulate)
    return self
