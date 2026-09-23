def f6(x: torch.Tensor) -> torch.Tensor:
    x = f5(x, 2)
    torch._dynamo.graph_break()
    x = f5(x, 4)
    return x
