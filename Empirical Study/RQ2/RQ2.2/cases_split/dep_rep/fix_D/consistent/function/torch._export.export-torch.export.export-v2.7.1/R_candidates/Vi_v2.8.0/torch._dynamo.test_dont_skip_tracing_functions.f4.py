def f4(x: torch.Tensor) -> torch.Tensor:
    x = f5(x, 1)
    x = torch._dynamo.dont_skip_tracing(f6)(x)
    x = f5(x, 8)
    return x
