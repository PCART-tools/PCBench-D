def simple_autograd_function(a=1):
    torch.rand(3).requires_grad_(True).mean().backward()
    return a ** 2
