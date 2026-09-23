def _no_grad_uniform_(tensor, a, b, generator=None):
    with torch.no_grad():
        return tensor.uniform_(a, b, generator=generator)
