def _no_grad_zero_(tensor):
    with torch.no_grad():
        return tensor.zero_()
