def _no_grad_fill_(tensor, val):
    with torch.no_grad():
        return tensor.fill_(val)
