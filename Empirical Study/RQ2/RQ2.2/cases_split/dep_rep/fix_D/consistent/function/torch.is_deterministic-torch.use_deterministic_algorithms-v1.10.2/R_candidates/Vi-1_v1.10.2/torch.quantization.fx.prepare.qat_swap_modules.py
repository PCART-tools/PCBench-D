def qat_swap_modules(
        root: torch.nn.Module,
        additional_qat_module_mapping: Dict[Callable, Callable]) -> None:
    all_mappings = get_combined_dict(
        get_default_qat_module_mappings(), additional_qat_module_mapping)
    convert(root, mapping=all_mappings, inplace=True, remove_qconfig=False)
