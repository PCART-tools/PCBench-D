def _get_unique_module_name(module_names: dict[str, int], module_name: str) -> str:
    module_names.setdefault(module_name, 0)
    module_names[module_name] += 1
    return f"{module_name}_{module_names[module_name]}"
