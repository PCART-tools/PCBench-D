def accumulate_grad(x, new_grad):
    if new_grad is None:
        return
    new_grad = torch.clone(new_grad)
    if x.grad is None:
        x.grad = new_grad
    else:
        x.grad.add_(new_grad)
