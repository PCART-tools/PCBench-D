def extract_parameters(node: _ProfilerEvent) -> Iterator[TensorKey]:
    for p, _p_grad in _extract_parameters_and_gradients(node):
        if p is not None:
            yield p
