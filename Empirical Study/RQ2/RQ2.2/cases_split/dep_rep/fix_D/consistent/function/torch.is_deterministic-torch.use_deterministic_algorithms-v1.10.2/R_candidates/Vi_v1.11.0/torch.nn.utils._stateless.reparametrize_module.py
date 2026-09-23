@contextlib.contextmanager
def reparametrize_module(
    module: torch.nn.Module,
    parameters_and_buffers: Dict[str, Tensor],
) -> Iterator[None]:
    for name, tensor in parameters_and_buffers.items():
        _apply_func_submodules(
            _swap_parameters,
            module, name.split("."), (tensor,))
    yield
    for name in parameters_and_buffers:
        _apply_func_submodules(
            _remove_swap,
            module, name.split("."), ())
