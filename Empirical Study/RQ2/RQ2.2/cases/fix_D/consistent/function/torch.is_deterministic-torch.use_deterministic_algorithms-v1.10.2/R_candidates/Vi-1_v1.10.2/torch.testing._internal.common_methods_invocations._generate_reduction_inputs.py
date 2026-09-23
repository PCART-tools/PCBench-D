def _generate_reduction_inputs(device, dtype, requires_grad):
    """Generates input tensors for testing reduction operators"""
    yield make_tensor([], device, dtype, requires_grad=requires_grad)
    yield make_tensor([2], device, dtype, requires_grad=requires_grad)
    yield make_tensor([3, 5], device, dtype, requires_grad=requires_grad, noncontiguous=True)
    yield make_tensor([3, 2, 1, 2], device, dtype, requires_grad=requires_grad)
