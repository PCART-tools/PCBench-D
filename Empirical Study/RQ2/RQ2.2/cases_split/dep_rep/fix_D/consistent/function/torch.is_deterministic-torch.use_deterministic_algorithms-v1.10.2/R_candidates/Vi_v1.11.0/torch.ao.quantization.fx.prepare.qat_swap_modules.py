def qat_swap_modules(
        root: torch.nn.Module,
        module_to_qat_module: Dict[Callable, Callable]) -> None:
    convert(root, mapping=module_to_qat_module, inplace=True, remove_qconfig=False)
