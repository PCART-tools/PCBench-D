def extract_gradients(
    node: _ProfilerEvent,
) -> Iterator[tuple[Optional[TensorKey], TensorKey]]:
    for p, p_grad in _extract_parameters_and_gradients(node):
        if p_grad is not None:
            yield p, p_grad
