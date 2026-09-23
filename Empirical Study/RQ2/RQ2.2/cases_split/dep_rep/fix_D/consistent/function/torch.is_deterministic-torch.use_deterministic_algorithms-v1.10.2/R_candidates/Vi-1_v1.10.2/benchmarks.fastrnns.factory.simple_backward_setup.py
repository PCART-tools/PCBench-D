def simple_backward_setup(output, seed=None):
    assert isinstance(output, torch.Tensor)
    if seed:
        torch.manual_seed(seed)
    grad_output = torch.randn_like(output)
    return output, grad_output
