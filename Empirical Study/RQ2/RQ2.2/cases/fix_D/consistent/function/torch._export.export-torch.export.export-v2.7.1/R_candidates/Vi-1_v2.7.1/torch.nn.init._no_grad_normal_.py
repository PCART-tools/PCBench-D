def _no_grad_normal_(tensor, mean, std, generator=None):
    with torch.no_grad():
        return tensor.normal_(mean, std, generator=generator)
