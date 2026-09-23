def is_parameter_freezing():
    return torch._inductor.config.freezing and not torch.is_grad_enabled()
