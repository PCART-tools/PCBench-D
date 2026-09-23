def f5(x: torch.Tensor, n: int) -> torch.Tensor:
    if torch.compiler.is_compiling():
        return x + n
    return x
