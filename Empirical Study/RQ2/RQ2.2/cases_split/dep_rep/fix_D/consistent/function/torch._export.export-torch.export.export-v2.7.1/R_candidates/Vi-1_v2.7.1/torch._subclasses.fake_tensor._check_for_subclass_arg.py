def _check_for_subclass_arg(x: object) -> bool:
    return (
        not isinstance(x, FakeTensor)
        and isinstance(x, Tensor)
        and type(x) is not Tensor
        and type(x) is not torch.nn.Parameter
    )
