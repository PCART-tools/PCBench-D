def validate_subgraph_args_types(lifted_args: Union[tuple[Any, ...], list[Any]]):
    allowed_types = (torch.Tensor, int, torch.SymInt)
    assert all(
        isinstance(arg, (torch.Tensor, int, torch.SymInt)) for arg in lifted_args
    ), f"{lifted_args} can only be of {allowed_types} but got {tuple(type(arg) for arg in lifted_args)}"
