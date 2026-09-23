def _apply_func_submodules(
    func: Callable[..., None],
    module: torch.nn.Module,
    path: List[str],
    args: Tuple,
):
    if len(path) == 1:
        func(module, path[0], *args)
    else:
        _apply_func_submodules(func, getattr(module, path[0]), path[1:], args)
